# Generated by Django 4.2 on 2023-06-13 21:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('police', '0007_alter_registerpolice_foto_alter_registerpolice_posto'),
    ]

    operations = [
        migrations.AlterField(
            model_name='registerpolice',
            name='telefone',
            field=models.CharField(max_length=20),
        ),
    ]