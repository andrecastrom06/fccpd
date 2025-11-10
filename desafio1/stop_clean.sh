#!/bin/sh
docker-compose down --rmi local --volumes --remove-orphans
docker network rm desafio_net 2>/dev/null || true
echo "Parado e limpo."
