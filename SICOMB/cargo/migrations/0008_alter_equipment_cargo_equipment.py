# Generated by Django 4.2 on 2023-06-12 03:18

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('equipment', '0019_remove_equipment_observation'),
        ('cargo', '0007_remove_equipment_cargo_bullet_amount_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='equipment_cargo',
            name='equipment',
            field=models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='equipment.equipment'),
        ),
    ]