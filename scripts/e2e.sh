#!/bin/sh
# Full end-to-end test of the Docker stack: build, health, smoke test through nginx,
# then a real backup -> change -> restore cycle with checksum verification.
#
#   ENV_FILE=<env file> COMPOSE_PROJECT_NAME=<isolated name> scripts/e2e.sh
#
# Uses its own Compose project (and therefore its own volumes); removes it afterwards.
# The env file must set DJANGO_SUPERUSER_EMAIL / _PASSWORD; HTTP_PORT selects the nginx port.
set -eu

: "${ENV_FILE:?set ENV_FILE to an env file for the test stack}"
: "${COMPOSE_PROJECT_NAME:=flask-e2e}"
export ENV_FILE COMPOSE_PROJECT_NAME
set -a; . "$ENV_FILE"; set +a
export BASE_URL="http://localhost:${HTTP_PORT:-80}"

cleanup() {
    status=$?
    if [ "$status" -ne 0 ]; then
        echo "== FAILED (exit $status): container logs" >&2
        docker compose logs --no-color --tail 200 >&2 || true
    fi
    docker compose down -v --remove-orphans > /dev/null 2>&1 || true
}
trap cleanup EXIT

echo "== build and start (waits for all health checks)"
docker compose up -d --build --wait

echo "== smoke test"
state=$(python3 scripts/smoke_test.py check)
attachment=$(printf '%s' "$state" | python3 -c 'import json,sys; print(json.load(sys.stdin)["attachment"])')
checksum=$(printf '%s' "$state" | python3 -c 'import json,sys; print(json.load(sys.stdin)["sha256"])')

echo "== backup"
docker compose exec -T backup sh /scripts/backup.sh
backup=$(docker compose exec -T backup sh -c 'ls -1 /backups | grep -E "^20.*Z$" | tail -1')

echo "== change data after the backup"
python3 scripts/smoke_test.py marker "created after backup"
python3 scripts/smoke_test.py titles | grep -q "created after backup"

echo "== restore $backup"
sh scripts/restore.sh "$backup" --yes

echo "== verify the restored state"
titles=$(python3 scripts/smoke_test.py titles)
echo "$titles" | grep -q "Smoke test project" || { echo "FAIL: restored data missing" >&2; exit 1; }
if echo "$titles" | grep -q "created after backup"; then echo "FAIL: post-backup change survived the restore" >&2; exit 1; fi
restored=$(python3 scripts/smoke_test.py download "$attachment")
[ "$restored" = "$checksum" ] || { echo "FAIL: restored attachment differs" >&2; exit 1; }

echo "== all end-to-end checks passed"
