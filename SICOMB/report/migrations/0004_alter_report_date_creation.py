# Generated by Django 5.0 on 2024-01-09 18:08

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('report', '0003_alter_report_date_creation_alter_report_title'),
    ]

    operations = [
        migrations.AlterField(
            model_name='report',
            name='date_creation',
            field=models.DateTimeField(default=datetime.datetime(2024, 1, 9, 15, 8, 25, 259398)),
        ),
    ]