# Generated by Django 3.2.14 on 2022-08-04 07:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('raids', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='raidhistory',
            name='time_limit',
            field=models.PositiveIntegerField(),
        ),
    ]