# Generated by Django 3.1.7 on 2021-02-20 13:32

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('arbeitsstunden', '0002_auto_20210214_1304'),
    ]

    operations = [
        migrations.AddField(
            model_name='arbeitseinheit',
            name='Datum',
            field=models.DateField(default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]