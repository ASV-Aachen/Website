# Generated by Django 3.1.6 on 2021-02-13 07:51

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='InfoPage',
            fields=[
                ('Titel', models.CharField(max_length=200, primary_key=True, serialize=False)),
                ('Text', models.TextField()),
                ('Beschreibung', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Jahresinfo',
            fields=[
                ('Jahr', models.IntegerField(primary_key=True, serialize=False)),
                ('ZuLeistendeArbeitsstunden', models.IntegerField()),
            ],
        ),
    ]