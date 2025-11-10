#!/bin/sh
SERVER_HOST="${SERVER_HOST:-server}"
INTERVAL="${INTERVAL:-5}"

while true; do
  echo "--- $(date --rfc-3339=seconds) - Requesting http://${SERVER_HOST}:8080/ ---"
  curl -s -o /dev/null -w "HTTP %{http_code}\n" "http://${SERVER_HOST}:8080/" || echo "curl failed"
  sleep "$INTERVAL"
done
