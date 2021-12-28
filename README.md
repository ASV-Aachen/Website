# Website
Repo für die Website des ASV Aachen. 

[![CodeQL](https://github.com/ASV-Aachen/Website/actions/workflows/codeql-analysis.yml/badge.svg?branch=main)](https://github.com/ASV-Aachen/Website/actions/workflows/codeql-analysis.yml)
[![OSSAR](https://github.com/ASV-Aachen/Website/actions/workflows/ossar-analysis.yml/badge.svg?branch=main)](https://github.com/ASV-Aachen/Website/actions/workflows/ossar-analysis.yml)
[![Test and publish a Django image](https://github.com/ASV-Aachen/Website/actions/workflows/testAndPublish.yml/badge.svg?branch=main)](https://github.com/ASV-Aachen/Website/actions/workflows/testAndPublish.yml)

## Development Guide
Zum Testen kann die Website im Deployment gestartet werden, siehe Repo _Deployment_

Alle Adressen sind nur noch unter https erreichbar.
### Scripts

* Wer unter Windows entwickelt und keine Makefiles ausfuehren kann, kann in die Makefile schauen oder in den `./bin/` Ordner. Dort sind alle commands gelistet.
* Die Batch-Skripte können genutzt werden, um die Befehle unter Windows auszuführen (Beispiel: `./bin/start.bat`)

### Entwicklung mit Docker Containern
Der Quellcode-Ordner `Webpage` wird als Volume in den Webpage-Container eingebunden, sodass Änderungen ohne neustarten des Containers vom Django-Server übernommen werden. Werden Änderungen an Models vorgenommen, können diese mit `make makemigrations` und anschließendem `make migrate` eingepflegt werden. Die Migrationen sind danach auch im Quellcode-Ordner verfügbar und können (bzw. sollten) mit committet werden.

Mehr zu Migrationen steht hier: https://docs.djangoproject.com/en/3.1/topics/migrations/

### Namenskonventionen für Apps, Modelle Variablen etc. 
* Alle Begriffe im Backend für Apps, Variablen Modelle etc. werden in englisch ohne Großbuchstaben beschrieben.
* Alle für den User sichtbare Begriffe im Frontend wie Links, Menüepunkte etc. werden in deutsch, die urls ohne Großbuchstaben, definiert.

