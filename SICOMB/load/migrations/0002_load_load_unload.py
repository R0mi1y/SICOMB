# Generated by Django 4.2.5 on 2023-10-12 14:45

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('load', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='load',
            name='load_unload',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.SET_NULL, to='load.load'),
        ),
    ]