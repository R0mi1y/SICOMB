# Generated by Django 4.2.5 on 2023-12-09 16:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('police', '0004_police_activator'),
    ]

    operations = [
        migrations.AlterField(
            model_name='police',
            name='tipo',
            field=models.CharField(choices=[('Policial', 'Policial'), ('Adjunto', 'Adjunto'), ('Admin', 'Admin')], default='Police', max_length=20),
        ),
    ]
