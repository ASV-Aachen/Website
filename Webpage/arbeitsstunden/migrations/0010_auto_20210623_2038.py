# Generated by Django 3.1.12 on 2021-06-23 20:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('arbeitsstunden', '0009_auto_20210623_2002'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project',
            name='tags',
            field=models.ManyToManyField(blank=True, to='arbeitsstunden.tag'),
        ),
    ]