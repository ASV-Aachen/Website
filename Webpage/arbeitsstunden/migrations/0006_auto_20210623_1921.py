# Generated by Django 3.1.12 on 2021-06-23 19:21

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('arbeitsstunden', '0005_auto_20210616_1756'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='work',
            name='date',
        ),
        migrations.RemoveField(
            model_name='work',
            name='description',
        ),
        migrations.AddField(
            model_name='project',
            name='parts',
            field=models.ManyToManyField(blank=True, to='arbeitsstunden.work'),
        ),
        migrations.AddField(
            model_name='work',
            name='endDate',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='work',
            name='name',
            field=models.CharField(default='NameNeeded', max_length=256),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='work',
            name='startDate',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='work',
            name='voluntary',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='project',
            name='responsible',
            field=models.ManyToManyField(blank=True, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='project',
            name='tags',
            field=models.ManyToManyField(blank=True, to='arbeitsstunden.tag'),
        ),
        migrations.DeleteModel(
            name='subproject',
        ),
    ]
