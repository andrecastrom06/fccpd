#!/bin/sh
docker-compose build
docker-compose up -d
echo "Containers subiram. Use ./stop_clean.sh para parar e remover."
