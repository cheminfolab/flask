#!/bin/sh
# Restore a backup into the running Compose stack. Run from the repository root:
#
#   scripts/restore.sh --list                 show available backups
#   scripts/restore.sh <backup name> --yes    REPLACE the database and files with that backup
#
# The backup must be in the `backups` volume. To restore an off-site copy, first copy it in:
#   docker compose cp ./2026-11-04T023000Z backup:/backups/
set -eu

compose="docker compose"

if [ "${1:-}" = "--list" ] || [ $# -eq 0 ]; then
    $compose exec -T backup sh -c 'ls -1 /backups | grep -E "^20.*Z$" || echo "(no backups yet)"; echo "last success: $(cat /backups/LAST_SUCCESS 2>/dev/null || echo never)"'
    exit 0
fi

name="$1"
if [ "${2:-}" != "--yes" ]; then
    echo "This replaces ALL current data (database, images, attachments) with backup $name." >&2
    echo "Re-run with --yes to continue: scripts/restore.sh $name --yes" >&2
    exit 1
fi

echo "stopping the application"
$compose stop nginx backend backup

echo "restoring $name"
if ! $compose run --rm restore "$name"; then
    echo "RESTORE FAILED. The application is stopped; fix the problem and re-run, or start it with:" >&2
    echo "  $compose up -d" >&2
    exit 1
fi

echo "starting the application"
$compose up -d --wait backend nginx backup

echo "verifying attachments against their recorded checksums"
$compose exec -T backend python manage.py verify_attachments
