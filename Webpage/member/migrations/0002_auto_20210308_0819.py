# Generated by Django 3.1.7 on 2021-03-08 08:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('member', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='status',
            field=models.PositiveSmallIntegerField(blank=True, choices=[(1, 'Anwärter'), (2, 'Aktiv'), (3, 'Inaktiv'), (4, 'AlterHerr')], null=True),
        ),
    ]