# Generated by Django 3.1.7 on 2021-04-05 21:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0005_auto_20210405_1118'),
    ]

    operations = [
        migrations.AlterField(
            model_name='infopage',
            name='name',
            field=models.CharField(max_length=200),
        ),
    ]