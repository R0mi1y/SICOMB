# Generated by Django 4.2.5 on 2023-09-19 23:38

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('equipment', '0008_bullet_activated_equipment_activated_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='equipment',
            name='date_register',
            field=models.DateTimeField(default=django.utils.timezone.now, verbose_name='Data de registro'),
        ),
    ]
