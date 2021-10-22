pip3 install -r requirements.txt
cd Webpage
python3 manage.py test --settings=Django.settings.test

rm db.sqlite3