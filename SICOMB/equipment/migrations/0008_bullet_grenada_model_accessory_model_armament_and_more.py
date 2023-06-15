# Generated by Django 4.2.1 on 2023-05-20 20:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('equipment', '0007_alter_equipment_serial_number'),
    ]

    operations = [
        migrations.CreateModel(
            name='Bullet',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.IntegerField(default=0, verbose_name='Quantidade')),
                ('image_path', models.TextField(default='', verbose_name='caminho da imagem')),
                ('caliber', models.CharField(max_length=50, verbose_name='Calibre')),
            ],
        ),
        migrations.CreateModel(
            name='Grenada',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('model', models.TextField(verbose_name='Modelo do armamento')),
                ('image_path', models.TextField(default='', verbose_name='caminho da imagem')),
            ],
        ),
        migrations.CreateModel(
            name='Model_accessory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('model', models.TextField(verbose_name='Modelo do armamento')),
            ],
        ),
        migrations.CreateModel(
            name='Model_armament',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('model', models.TextField(verbose_name='Modelo do armamento')),
                ('caliber', models.CharField(max_length=10, verbose_name='Calibre')),
                ('image_path', models.TextField(default='', verbose_name='caminho da imagem')),
            ],
        ),
        migrations.CreateModel(
            name='Model_wearable',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('model', models.TextField(verbose_name='Modelo do armamento')),
                ('size', models.CharField(max_length=10, verbose_name='Tamanho')),
                ('image_path', models.TextField(default='', verbose_name='caminho da imagem')),
            ],
        ),
        migrations.DeleteModel(
            name='Armament',
        ),
        migrations.DeleteModel(
            name='Wearable',
        ),
        migrations.AddField(
            model_name='equipment',
            name='observation',
            field=models.TextField(default='null', verbose_name='Observação'),
        ),
        migrations.AddField(
            model_name='equipment',
            name='status',
            field=models.CharField(default='Disponivel', max_length=10, verbose_name='Estado atual'),
        ),
        migrations.AlterField(
            model_name='equipment',
            name='serial_number',
            field=models.CharField(max_length=20, verbose_name='Numero de série'),
        ),
        migrations.AlterField(
            model_name='equipment',
            name='type',
            field=models.CharField(default='', max_length=50, verbose_name='Tipo'),
        ),
        migrations.AlterField(
            model_name='equipment',
            name='type_id',
            field=models.CharField(default='null', max_length=50, verbose_name='Tipo'),
        ),
        migrations.AlterField(
            model_name='equipment',
            name='uid',
            field=models.CharField(default='null', max_length=20, primary_key=True, serialize=False, verbose_name='UID'),
        ),
    ]