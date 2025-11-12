#!/bin/sh
SERVER_HOST="${SERVER_HOST:-server}"
INTERVAL="${INTERVAL:-5}"

while true; do
  echo "$(date '+%Y-%m-%d %H:%M:%S') -> Requisitando http://${SERVER_HOST}:8080/"
  curl -s -o /dev/null -w "HTTP %{http_code}\n" "http://${SERVER_HOST}:8080/" || echo "Falha no curl"
  sleep "$INTERVAL"
done