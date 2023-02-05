#!/bin/sh

cp -avr website/Webpage/static/ InitFiles/webpage/

docker-compose exec -T webpage python3 manage.py init