# Generated by Django 4.2 on 2023-06-16 14:14

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('equipment', '0002_bullet_model_accessory_model_armament_model_grenada_and_more'),
        ('cargo', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cargo',
            name='police',
        ),
        migrations.AddField(
            model_name='cargo',
            name='situation',
            field=models.CharField(default='Pendente', max_length=20, verbose_name='Devolvido'),
        ),
        migrations.AddField(
            model_name='cargo',
            name='status',
            field=models.CharField(default='Pendente', max_length=20, verbose_name='horário_carga'),
        ),
        migrations.AlterField(
            model_name='cargo',
            name='date_cargo',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name='cargo',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.CreateModel(
            name='Equipment_cargo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.IntegerField(default='1', null=True, verbose_name='Quantidade')),
                ('observation', models.TextField(default=None, null=True, verbose_name='Observação')),
                ('bullet', models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='equipment.bullet')),
                ('cargo', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cargo.cargo')),
                ('equipment', models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='equipment.equipment')),
            ],
        ),
    ]
