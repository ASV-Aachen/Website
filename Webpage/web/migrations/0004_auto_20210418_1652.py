# Generated by Django 3.1.8 on 2021-04-18 16:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0003_auto_20210418_0854'),
    ]

    operations = [
        migrations.AlterField(
            model_name='headpage',
            name='name',
            field=models.CharField(max_length=200, unique=True),
        ),
        migrations.AlterField(
            model_name='infopagehistory',
            name='name',
            field=models.CharField(max_length=200),
        ),
    ]