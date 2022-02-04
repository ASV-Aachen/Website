# Website
Repo für die Website des ASV Aachen. 

[![CodeQL](https://github.com/ASV-Aachen/Website/actions/workflows/codeql-analysis.yml/badge.svg)](https://github.com/ASV-Aachen/Website/actions/workflows/codeql-analysis.yml)
[![OSSAR](https://github.com/ASV-Aachen/Website/actions/workflows/ossar-analysis.yml/badge.svg)](https://github.com/ASV-Aachen/Website/actions/workflows/ossar-analysis.yml)
[![Publish a Django image](https://github.com/ASV-Aachen/Website/actions/workflows/Publish.yml/badge.svg)](https://github.com/ASV-Aachen/Website/actions/workflows/Publish.yml)

# Development Guide
Zum Testen kann die Website in einem Docker Netz aufgesetzt werden. Hierfür gibt es ein eigenes [Repo](https://github.com/ASV-Aachen/development) für ASVer welches extra entsprechend configuriert ist um eine Weiterentwicklung der Komponenten möglichst einfach zu gestalten.

## Die Website einzeln deployen
Die Website benötigt weitere Services wie Keycloak und eine MySQL Datenbank.

Das Package selbst kann ohne Anpassungen deployed werden. Hierfür müssen nur einige Einstellungen configuriert werden:
``
    environment: 
      # Einstellung für den Client im Keycloak. 
      OIDC_RP_CLIENT_ID: 'website'
      OIDC_RP_SIGN_ALGO: 'RS256'
      OIDC_RP_CLIENT_SECRET: 'b21fc13e-46b0-49ff-836e-89bf413f85ee'
      # Einstellungen für die Verbindung zum Keycloak
      # Host muss in der Form "http://HOSTNAME:PORT" gesetzt werden. ACHTUNG, kein Localhost. Im Zweifel den Namen des Computers im Netzwerk nutzen.
      Host: 'http://localhost'
      ALLOWED_HOSTS: "localhost"
      KEYCLOAK_USER: admin
      KEYCLOAK_PASSWORD: Pa55w0rd
      
      # Secret Key fürs Django
      SECRET_KEY: '+p32r=0@5ab%chynmfculz8bm9yyo_ot7-3q1-!#8+t0z*llz!'
      
      #MYSQL
      MYSQL_USER: website
      MYSQL_PASSWORD: my-secret-pw
      DEBUG: "True"
      
``

Der Container wird mit folgendem Kommando gestartet:     
``
command: >
      bash -c "update-ca-certificates && python manage.py runserver 0.0.0.0:8080"
``

Es empfiehlt sich Volumes anzulegen um Uploads wie Bilder auch persistent zu speichern. 

**WICHTIG**

Alle Adressen sind nur noch unter https erreichbar.


### Scripts

* Wer unter Windows entwickelt und keine Makefiles ausfuehren kann, kann in die Makefile schauen oder in den `./bin/` Ordner. Dort sind alle commands gelistet.
* Die Batch-Skripte können genutzt werden, um die Befehle unter Windows auszuführen (Beispiel: `./bin/start.bat`)

### Namenskonventionen für Apps, Modelle Variablen etc. 
* Alle Begriffe im Backend für Apps, Variablen Modelle etc. werden in englisch ohne Großbuchstaben beschrieben.
* Alle für den User sichtbare Begriffe im Frontend wie Links, Menüepunkte etc. werden in deutsch, die urls ohne Großbuchstaben, definiert.

