# Website
Repo für die Website des ASV Aachen
Alle Adressen sind nur noch unter https erreichbar

## First Start
### SSO
Beim ersten Start vom Keycloak müssen einige Einstellungen angepasst werden:
1. Keycloak Admin Console unter "/sso/auth" öffnen und mit den Zugangsdaten für den Admin aus der Docker-Compose einloggen.
2. der Realm ASV sollte bereits geladen sein. Falls nicht muss die Realm.json Datei importiert werden (unten links gibt es einen Import Button), die entsprechende Datei liegt unter initfiles/sso/realms.json. 
3. Unter User muss ein erster Nutzer angelegt werden. Auch wenn nur das Feld "Username" als required markiert ist sind "Email" und "Password" (unter Credentials) erforderlich.
4. Look and Feel ist auf ASV angepasst. Hierzu unter General die Themen "asv" und die deutsche Sprache als Standard ausgewählen. Überschriften anpassen: 
> - ASV Realm: Name: ASV; Anzeigename und HTML-Anzeigebereich: "Mitgliederbereich". 
> - Master Realm: General: Name: ASV; Anzeigename und HTML-Anzeigebereich: "Nutzermanagement". 
Das Thema kann im Ordner "InitFiles/sso/thems/asv" weiter customized werden.       
5. Keycloak ist fertig eingerichtet. Zum Testen kann man sich unter "/login" anmelden. Der Django User wird dabei beim ersten Anmelden automatisch erstellt. 

### Website

#### Verbindung zum SSO
1. Unter Clients -> Website -> Credentials muss ein neues Secret erstellt werden (Button rechts daneben)
1. `docker-compose.override.yml` Datei erstellen und folgenden Inhalt dort hinein kopieren:
```
version: '3.7'

services:
  #---------------------------------------------------------------------------------------
  # Proxy
  #---------------------------------------------------------------------------------------

  reverse-proxy:
    ports:
      # The HTTP port
      - "80:80"
      # HTTPS
      - "443:443"
      # The Web UI (enabled by --api.insecure=true)
      - "8080:8080"


  #---------------------------------------------------------------------------------------
  # Datenbank
  #---------------------------------------------------------------------------------------
  db:
    environment:
      MYSQL_ROOT_PASSWORD: "my-secret-pw"
      MYSQL_ROOT_HOST: "localhost"


  #---------------------------------------------------------------------------------------
  # Nextcloud
  #---------------------------------------------------------------------------------------

  cloud:
    environment:
      #DB
      MYSQL_USER: Nextcloud
      MYSQL_PASSWORD: my-secret-pw
      #Admin
      NEXTCLOUD_ADMIN_USER: admin
      NEXTCLOUD_ADMIN_PASSWORD: Pa55w0rd
      #Redis
      REDIS_HOST: nextcloud-redis
      REDIS_HOST_PASSWORD: my-secret-pw


  #---------------------------------------------------------------------------------------
  # SSO - Keycloak
  #---------------------------------------------------------------------------------------

  SSO:
    environment:
      # DB Settings
      DB_USER: Keycloack
      DB_PASSWORD: my-secret-pw
      # Keycloack Admin Settings
      KEYCLOAK_USER: admin
      KEYCLOAK_PASSWORD: Pa55w0rd


  #---------------------------------------------------------------------------------------
  # Webpage
  #---------------------------------------------------------------------------------------

  webpage:
    environment:
      OIDC_RP_CLIENT_SECRET: '******'
      # Einstellungen für die Verbindung zum Keycloak
      # Host muss in der Form "https://HOSTNAME" gesetzt werden. ACHTUNG, kein Localhost. Im Zweifel den Namen des Computers im Netzwerk nutzen.
      Host: https://***
      ALLOWED_HOSTS: "***"
      KEYCLOAK_USER: admin
      KEYCLOAK_PASSWORD: Pa55w0rd
      # Secret Key fürs Django
      SECRET_KEY: '+p32r=0@5ab%chynmfculz8bm9yyo_ot7-3q1-!#8+t0z*llz!'
      #MYSQL
      MYSQL_USER: website
      MYSQL_PASSWORD: my-secret-pw

```
1. Secret kopieren und in dieser Docker-Compose Datei unter __OIDC_RP_CLIENT_SECRET__ eintragen.
1. __Host__ und __ALLOWED_HOSTS__ in der Docker-Compose eintragen.
1. Website neu starten

**ACHTUNG: ** In der aktuellen Version arbeiten wir mit HTTPS!!!

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
firstStart                     Creates the init Data for the Website 
```

* Wer unter Windows entwickelt und keine Makefiles ausfuehren kann, kann in die Makefile schauen oder in den `./bin/` Ordner. Dort sind alle commands gelistet.
* Die Batch-Skripte können genutzt werden, um die Befehle unter Windows auszuführen (Beispiel: `./bin/start.bat`)

### Entwicklung mit Docker Containern
Der Quellcode-Ordner `Webpage` wird als Volume in den Webpage-Container eingebunden, sodass Änderungen ohne neustarten des Containers vom Django-Server übernommen werden. Werden Änderungen an Models vorgenommen, können diese mit `make makemigrations` und anschließendem `make migrate` eingepflegt werden. Die Migrationen sind danach auch im Quellcode-Ordner verfügbar und können (bzw. sollten) mit committet werden.

Mehr zu Migrationen steht hier: https://docs.djangoproject.com/en/3.1/topics/migrations/

### Namenskonventionen für Apps, Modelle Variablen etc. 
* Alle Begriffe im Backend für Apps, Variablen Modelle etc. werden in englisch ohne Großbuchstaben beschrieben.
* Alle für den User sichtbare Begriffe im Frontend wie Links, Menüepunkte etc. werden in deutsch, die urls ohne Großbuchstaben, definiert.





