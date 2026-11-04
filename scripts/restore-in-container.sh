#!/bin/sh
# Restores one backup, inside the `restore` tool container. Called by scripts/restore.sh.
set -eu

name="${1:?usage: restore-in-container.sh <backup name, e.g. 2026-11-04T023000Z>}"
source="/backups/$name"
export PGPASSWORD="${POSTGRES_PASSWORD:?}"

[ -f "$source/SHA256SUMS" ] || { echo "no backup at $source" >&2; exit 1; }
echo "verifying checksums"
(cd "$source" && sha256sum -c SHA256SUMS)

echo "restoring database $POSTGRES_DB"
pg_restore --clean --if-exists --no-owner --exit-on-error \
    --username="$POSTGRES_USER" --dbname="$POSTGRES_DB" "$source/database.dump"

echo "restoring files"
find /data/media /data/private_media -mindepth 1 -delete
tar -C /data -xzf "$source/files.tar.gz"
echo "restore of $name complete"
