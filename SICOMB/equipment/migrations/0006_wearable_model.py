# Generated by Django 4.2 on 2023-05-07 16:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('equipment', '0005_delete_armament_model_delete_wearble_model_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='wearable',
            name='model',
            field=models.TextField(default=None, verbose_name='Modelo do armamento'),
            preserve_default=False,
        ),
    ]
