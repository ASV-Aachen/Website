# Generated by Django 3.2.10 on 2021-12-19 12:57

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('arbeitsstunden', '0018_auto_20210718_1120'),
        ('cruises', '0003_delete_cruiseb'),
    ]

    operations = [
        migrations.CreateModel(
            name='sailor',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('isNew', models.BooleanField(default=False)),
                ('name', models.CharField(default='TESTNUTZER', max_length=256)),
            ],
        ),
        migrations.RemoveField(
            model_name='cruiseshare',
            name='profile',
        ),
        migrations.AddField(
            model_name='cruiseshare',
            name='cosailor',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.RESTRICT, to='arbeitsstunden.account'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='cruise',
            name='sailors',
            field=models.ManyToManyField(blank=True, null=True, through='cruises.cruiseShare', to='arbeitsstunden.account'),
        ),
    ]