#!/bin/sh
# Entrypoint of the `backup` service: runs scripts/backup.sh every day at BACKUP_TIME
# (local time of TIME_ZONE), and once at start unless BACKUP_ON_START=false.
# A failed run is logged and retried at the next scheduled time; the container's
# health check turns unhealthy when the last success is older than 26 hours.
set -u

export TZ="${TIME_ZONE:-UTC}"
time_of_day="${BACKUP_TIME:-02:30}"

run() {
    if sh /scripts/backup.sh; then
        :
    else
        echo "backup FAILED (exit $?); next attempt at $time_of_day" >&2
    fi
}

echo "backup service: daily at $time_of_day ($TZ), keeping ${BACKUP_KEEP_DAYS:-14} days"
touch /tmp/backup-service-started   # health check grace period after (re)start
[ "${BACKUP_ON_START:-true}" = "true" ] && run

while true; do
    now=$(date +%s)
    next=$(date -d "today $time_of_day" +%s)
    [ "$next" -le "$now" ] && next=$(date -d "tomorrow $time_of_day" +%s)
    sleep $((next - now))
    run
done
