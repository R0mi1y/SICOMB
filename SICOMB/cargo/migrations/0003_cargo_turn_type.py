# Generated by Django 4.2 on 2023-06-16 15:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cargo', '0002_remove_cargo_police_cargo_situation_cargo_status_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='cargo',
            name='turn_type',
            field=models.CharField(default='6H', max_length=20),
            preserve_default=False,
        ),
    ]
