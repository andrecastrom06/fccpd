#!/bin/sh
case "$1" in
  stop)
    docker-compose down --rmi local --volumes --remove-orphans
    docker network rm desafio_net 2>/dev/null || true
    echo "Containers parados e limpos."
    ;;
  *)
    docker-compose build
    docker-compose up -d
    echo "Containers subiram. Use '$0 stop' para parar e limpar."
    ;;
esac