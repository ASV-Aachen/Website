# Website
Repo für die Website des ASV Aachen

## First Start
### SSO
Beim ersten Start vom Keycloak müssen einige Einstellungen angepasst werden:
1. Keycloak Admin Console unter "/sso/auth" öffnen und mit den Zugangsdaten für den Admin aus der Docker-Compose einloggen.
1. der Realm ASV sollte bereits geladen sein. Falls nicht muss die Realm.json Datei importiert werden (unten links gibt es einen Import Button), die entsprechende Datei liegt unter initfiles/sso/realms.json. 
1. Unter User muss ein erster Nutzer angelegt werden. Auch wenn nur das Feld "Username" als required markiert ist sind "Email" und "Password" (unter Credentials) erforderlich.  
1. Keycloak ist fertig eingerichtet. Zum Testen kann man sich unter "/login" anmelden. Der Django User wird dabei beim ersten Anmelden automatisch erstellt. 

### Website

#### Verbindung zum SSO
1. Unter Clients -> Website -> Credentials muss ein neues Secret erstellt werden (Button rechts daneben)
1. `docker-compose.override.yml` Datei erstellen und folgenden Inhalt dort hinein kopieren:
```
version: '3.7'

services:  
  webpage:
    environment: 
      # Einstellungen für die Verbindung zum Keycloak
      # Host muss in der Form "http://HOSTNAME:PORT" gesetzt werden. 
      # ACHTUNG, kein Localhost. Im Zweifel den Namen des Computers im Netzwerk nutzen. 
      Host: http://192.168.0.XXX:11100
      ALLOWED_HOSTS: "192.168.0.XXX"

      # Einstellung für den Client im Keycloak. 
      OIDC_RP_CLIENT_SECRET: 'xxx-xxx-x-xx'

```
1. Secret kopieren und in dieser Docker-Compose Datei unter __OIDC_RP_CLIENT_SECRET__ eintragen.
1. __Host__ und __ALLOWED_HOSTS__ in der Docker-Compose eintragen.
1. Website neu starten
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
* Die Batch-Skripte können genutzt werden, um die Befehle unter Windows auszuführen (Beispiel: `./bin/start.bat`)

### Entwicklung mit Docker Containern
Der Quellcode-Ordner `Webpage` wird als Volume in den Webpage-Container eingebunden, sodass Änderungen ohne neustarten des Containers vom Django-Server übernommen werden. Werden Änderungen an Models vorgenommen, können diese mit `make makemigrations` und anschließendem `make migrate` eingepflegt werden. Die Migrationen sind danach auch im Quellcode-Ordner verfügbar und können (bzw. sollten) mit committet werden.

Mehr zu Migrationen steht hier: https://docs.djangoproject.com/en/3.1/topics/migrations/


