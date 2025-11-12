#!/bin/sh
case "$1" in
  stop)
    docker-compose down -v
    echo "Container parado e volume removido (limpeza completa)."
    ;;
  *)
    docker-compose up -d
    echo "Banco iniciado. Use '$0 stop' para parar e limpar tudo."
    ;;
esac