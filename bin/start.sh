#!/bin/sh

# Zum root verzeichnis wechseln


#-------------------------
# Bau das Netzwerk
docker network create traefik

#-------------------------
# Bau des WebpageImage
docker build -t webpageimage:0.1 .

#-------------------------
# Starte Docker compose
docker-compose up -d