# Website
Repo für die Website des ASV Aachen

## First Start
### SSO
Beim ersten Start vom Keycloak müssen einige Einstellungen angepasst werden:
1. Keycloak Admin Console unter "/sso/auth" öffnen und mit den Zugangsdaten für den Admin aus der Docker-Compose einloggen.
1. der Realm ASV sollte bereits geladen sein. Falls nicht muss die Realm.json Datei importiert werden (unten links gibt es einen Import Button), die entsprechende Datei liegt unter initfiles/sso/realms.json. 
1. Unter User muss ein erster Nutzer angelegt werden. 
1. Keycloak ist fertig eingerichtet. Zum Testen kann man sich unter "/login" anmelden. Der Django User wird dabei beim ersten Anmelden automatisch erstellt. 

### Website
#### Admin
Wird ein Keycloak Nutzer beim ersten anmelden neu erstellt, haben diese zunächst keinerlei Rechte. Es muss also ein Superuser manuell eingerichtet werden, welcher das erste bearbeiten übernimmt. Sobald man einen weiteren Admin bestimmt hat, kann dieser Account aber gelöscht werden.
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


