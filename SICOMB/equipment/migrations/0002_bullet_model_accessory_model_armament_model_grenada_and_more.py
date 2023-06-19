# Generated by Django 4.2 on 2023-06-19 14:33

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('equipment', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Bullet',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.IntegerField(default=0, verbose_name='Quantidade')),
                ('image_path', models.TextField(default='', verbose_name='caminho da imagem')),
                ('caliber', models.CharField(max_length=50, verbose_name='Calibre')),
                ('description', models.TextField(verbose_name='Descrição')),
            ],
        ),
        migrations.CreateModel(
            name='Model_accessory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('model', models.TextField(verbose_name='Modelo do armamento')),
                ('description', models.TextField(verbose_name='Descrição')),
                ('image_path', models.TextField(default='', verbose_name='caminho da imagem')),
            ],
        ),
        migrations.CreateModel(
            name='Model_armament',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('model', models.TextField(verbose_name='Modelo do armamento')),
                ('caliber', models.CharField(max_length=10, verbose_name='Calibre')),
                ('image_path', models.TextField(default='', verbose_name='caminho da imagem')),
                ('description', models.TextField(verbose_name='Descrição')),
            ],
        ),
        migrations.CreateModel(
            name='Model_grenada',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('model', models.TextField(verbose_name='Modelo do armamento')),
                ('image_path', models.TextField(default='', verbose_name='caminho da imagem')),
                ('description', models.TextField(verbose_name='Descrição')),
            ],
        ),
        migrations.CreateModel(
            name='Model_wearable',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('model', models.TextField(verbose_name='Modelo do armamento')),
                ('size', models.CharField(max_length=10, verbose_name='Tamanho')),
                ('image_path', models.TextField(default='', verbose_name='caminho da imagem')),
                ('description', models.TextField(verbose_name='Descrição')),
            ],
        ),
        migrations.RemoveField(
            model_name='wearable',
            name='equipment_uid',
        ),
        migrations.RemoveField(
            model_name='equipment',
            name='description',
        ),
        migrations.RemoveField(
            model_name='equipment',
            name='image_path',
        ),
        migrations.RemoveField(
            model_name='equipment',
            name='type',
        ),
        migrations.AddField(
            model_name='equipment',
            name='status',
            field=models.CharField(default='Disponível', max_length=20, verbose_name='Estado atual'),
        ),
        migrations.AlterField(
            model_name='equipment',
            name='serial_number',
            field=models.CharField(max_length=20, verbose_name='Numero de série'),
        ),
        migrations.AlterField(
            model_name='equipment',
            name='uid',
            field=models.CharField(default=None, max_length=20, primary_key=True, serialize=False, verbose_name='uid'),
        ),
        migrations.DeleteModel(
            name='Armament',
        ),
        migrations.DeleteModel(
            name='Wearable',
        ),
        migrations.AddField(
            model_name='equipment',
            name='accessory',
            field=models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='equipment.model_accessory'),
        ),
        migrations.AddField(
            model_name='equipment',
            name='armament',
            field=models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='equipment.model_armament'),
        ),
        migrations.AddField(
            model_name='equipment',
            name='grenada',
            field=models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='equipment.model_grenada'),
        ),
        migrations.AddField(
            model_name='equipment',
            name='wearable',
            field=models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='equipment.model_wearable'),
        ),
    ]
