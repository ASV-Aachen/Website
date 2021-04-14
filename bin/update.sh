#!/bin/sh

git pull
make start
make makemigrations
make migrate