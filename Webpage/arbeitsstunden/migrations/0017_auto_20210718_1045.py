# Generated by Django 3.2.5 on 2021-07-18 10:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('arbeitsstunden', '0016_auto_20210718_1012'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project',
            name='responsible',
            field=models.ManyToManyField(blank=True, to='arbeitsstunden.account'),
        ),
        migrations.AlterField(
            model_name='project',
            name='tags',
            field=models.ManyToManyField(blank=True, to='arbeitsstunden.tag'),
        ),
    ]
