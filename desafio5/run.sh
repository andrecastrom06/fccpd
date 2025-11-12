#!/bin/sh
case "$1" in
  stop)
    docker-compose down -v
    echo "Containers parados e volumes removidos."
    ;;
  *)
    docker-compose up -d
    echo "Microsserviços iniciados:"
    echo " - Users:   http://localhost:5001/users"
    echo " - Orders:  http://localhost:5002/orders"
    echo " - Gateway: http://localhost:8000/"
    echo "Use '$0 stop' para parar e limpar tudo."
    ;;
esac
