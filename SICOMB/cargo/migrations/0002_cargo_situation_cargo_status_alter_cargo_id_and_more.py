# Generated by Django 4.2 on 2023-06-08 19:46

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('police', '0002_adjunto_remove_registerpolice_email_and_more'),
        ('cargo', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='cargo',
            name='situation',
            field=models.CharField(default='Pendente', max_length=20, verbose_name='Devolvido'),
        ),
        migrations.AddField(
            model_name='cargo',
            name='status',
            field=models.CharField(default=None, max_length=20, verbose_name='horário_carga'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='cargo',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='cargo',
            name='police',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='police.registerpolice'),
        ),
    ]