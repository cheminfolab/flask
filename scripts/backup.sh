#!/bin/sh
# One backup run, inside the `backup` container (see docker-compose.yml).
#
# Writes /backups/<UTC timestamp>/ with
#   database.dump   pg_dump custom format (restore with pg_restore)
#   files.tar.gz    media/ and private_media/ (substance images, experiment attachments)
#   SHA256SUMS      checksums of both
# The database is dumped first, then the files: every attachment row in the dump has
# its file in the archive (files uploaded meanwhile are included without a row).
# A run that fails leaves only a *.partial directory, which the next run removes.
set -eu

export PGPASSWORD="${POSTGRES_PASSWORD:?POSTGRES_PASSWORD is not set}"
: "${POSTGRES_USER:?}" "${POSTGRES_DB:?}"

stamp=$(date -u +%Y-%m-%dT%H%M%SZ)
target="/backups/$stamp"
work="$target.partial"

rm -rf /backups/*.partial
mkdir -p "$work"

echo "backup $stamp: dumping database $POSTGRES_DB"
pg_dump --format=custom --username="$POSTGRES_USER" --dbname="$POSTGRES_DB" --file="$work/database.dump"
pg_restore --list "$work/database.dump" > /dev/null          # the dump is readable

echo "backup $stamp: archiving files"
tar -C /data -czf "$work/files.tar.gz" media private_media
tar -tzf "$work/files.tar.gz" > /dev/null                     # the archive is readable

(cd "$work" && sha256sum database.dump files.tar.gz > SHA256SUMS)
mv "$work" "$target"
date -u +%Y-%m-%dT%H:%M:%SZ > /backups/LAST_SUCCESS

# retention: keep the last BACKUP_KEEP_DAYS days
keep="${BACKUP_KEEP_DAYS:-14}"
find /backups -mindepth 1 -maxdepth 1 -type d -name '20*Z' -mtime +"$keep" -exec rm -rf {} +

echo "backup $stamp: done ($(du -sh "$target" | cut -f1)); kept: $(find /backups -mindepth 1 -maxdepth 1 -type d -name '20*Z' | wc -l)"
