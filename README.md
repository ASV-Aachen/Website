# Website
Repo für die Website des ASV Aachen

## Development Guide

### Scripts und Makefile
`make help` um alle commands zu sehen
```
# Makefile Help #
clean                          clean containers and images
makemigrations                 Generate Migrations for Django models
migrate                        Migrate Django models
start                          Start network && build && docker-compose up
stop                           stop docker-compose and network
```

* Wer unter Windows entwickelt und keine Makefiles ausfuehren kann, kann in die Makefile schauen oder in den `./bin/` Ordner. Dort sind alle commands gelistet.
* Beispiel: `./bin/start` ( cd bin && sh start.sh funktioniert nicht )

### Entwicklung mit Docker Containern
Der Quellcode-Ordner `Webpage` wird als Volume in den Webpage-Container eingebunden, sodass Änderungen ohne neustarten des Containers vom Django-Server übernommen werden. Werden Änderungen an Models vorgenommen, können diese mit `make makemigrations` und anschließendem `make migrate` eingepflegt werden. Die Migrationen sind danach auch im Quellcode-Ordner verfügbar und können (bzw. sollten) mit committet werden.

Mehr zu Migrationen steht hier: https://docs.djangoproject.com/en/3.1/topics/migrations/
