# Generated by Django 4.2.5 on 2023-12-29 22:02

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('report', '0002_report_date_creation'),
    ]

    operations = [
        migrations.AlterField(
            model_name='report',
            name='date_creation',
            field=models.DateTimeField(default=datetime.datetime(2023, 12, 29, 19, 2, 56, 90857)),
        ),
        migrations.AlterField(
            model_name='report',
            name='title',
            field=models.CharField(default='Relatório %d/%m/%Y', max_length=256),
        ),
    ]