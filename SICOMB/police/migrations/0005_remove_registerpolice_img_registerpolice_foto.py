# Generated by Django 4.2.1 on 2023-06-13 03:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('police', '0004_remove_registerpolice_id_registerpolice_email_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='registerpolice',
            name='img',
        ),
        migrations.AddField(
            model_name='registerpolice',
            name='foto',
            field=models.FileField(default='xxxxx', upload_to='media/'),
            preserve_default=False,
        ),
    ]
