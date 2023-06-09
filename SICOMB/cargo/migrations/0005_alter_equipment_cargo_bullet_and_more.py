# Generated by Django 4.2 on 2023-06-09 23:17

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('equipment', '0016_alter_equipment_uid'),
        ('cargo', '0004_equipment_cargo'),
    ]

    operations = [
        migrations.AlterField(
            model_name='equipment_cargo',
            name='bullet',
            field=models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='equipment.bullet'),
        ),
        migrations.AlterField(
            model_name='equipment_cargo',
            name='cargo',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cargo.cargo'),
        ),
    ]
