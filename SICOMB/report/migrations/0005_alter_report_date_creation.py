# Generated by Django 4.1.3 on 2024-01-18 17:40

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('report', '0004_alter_report_date_creation'),
    ]

    operations = [
        migrations.AlterField(
            model_name='report',
            name='date_creation',
            field=models.DateTimeField(default=datetime.datetime(2024, 1, 18, 14, 40, 7, 995265)),
        ),
    ]