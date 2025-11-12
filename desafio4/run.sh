#!/bin/sh
case "$1" in
  stop)
    docker-compose down -v
    echo "Containers parados e volumes removidos."
    ;;
  *)
    docker-compose up -d
    echo "Microsserviços iniciados:"
    echo " - Service A: http://localhost:5001/users"
    echo " - Service B: http://localhost:6001/"
    echo "Use '$0 stop' para parar e limpar tudo."
    ;;
esac