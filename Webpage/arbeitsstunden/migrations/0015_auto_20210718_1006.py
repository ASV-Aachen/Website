# Generated by Django 3.2.5 on 2021-07-18 10:06

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('arbeitsstunden', '0014_auto_20210705_1948'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customhours',
            name='season',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='arbeitsstunden.season', unique=True),
        ),
        migrations.AlterField(
            model_name='customhours',
            name='used_account',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='arbeitsstunden.account', unique=True),
        ),
        migrations.AlterField(
            model_name='project',
            name='tags',
            field=models.ManyToManyField(blank=True, to='arbeitsstunden.tag'),
        ),
        migrations.AlterField(
            model_name='work',
            name='setupDate',
            field=models.DateField(default=datetime.date(2021, 7, 18)),
        ),
    ]