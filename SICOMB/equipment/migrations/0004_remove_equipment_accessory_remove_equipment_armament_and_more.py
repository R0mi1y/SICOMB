# Generated by Django 4.2.3 on 2023-08-18 23:15

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
        ('equipment', '0003_alter_equipment_serial_number'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='equipment',
            name='accessory',
        ),
        migrations.RemoveField(
            model_name='equipment',
            name='armament',
        ),
        migrations.RemoveField(
            model_name='equipment',
            name='grenada',
        ),
        migrations.RemoveField(
            model_name='equipment',
            name='wearable',
        ),
        migrations.AddField(
            model_name='equipment',
            name='model_id',
            field=models.PositiveIntegerField(default=None),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='equipment',
            name='model_type',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='contenttypes.contenttype'),
            preserve_default=False,
        ),
    ]
