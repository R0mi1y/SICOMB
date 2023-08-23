# Generated by Django 4.2.3 on 2023-08-22 18:39

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('equipment', '0004_remove_equipment_accessory_remove_equipment_armament_and_more'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Load',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_load', models.DateTimeField(default=django.utils.timezone.now)),
                ('expected_load_return_date', models.DateTimeField(null=True, verbose_name='Data Prevista de Devolução')),
                ('returned_load_date', models.DateTimeField(null=True, verbose_name='Data de Descarregamento')),
                ('turn_type', models.CharField(max_length=20)),
                ('status', models.CharField(default='Pendente', max_length=50, verbose_name='horário_carga')),
                ('police', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Equipment_load',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.IntegerField(default='1', null=True, verbose_name='Quantidade')),
                ('observation', models.TextField(default=None, null=True, verbose_name='Observação')),
                ('status', models.CharField(default='Aprovado', max_length=20, verbose_name='Status')),
                ('bullet', models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='equipment.bullet')),
                ('equipment', models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='equipment.equipment')),
                ('load', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='load.load')),
            ],
        ),
    ]
