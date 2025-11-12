#!/bin/sh
case "$1" in
  stop)
    docker-compose down -v
    echo "Containers parados e volumes removidos."
    ;;
  *)
    docker-compose up -d
    echo "Ambiente iniciado. Acesse http://localhost:8080"
    echo "Use '$0 stop' para parar e limpar tudo."
    ;;
esac