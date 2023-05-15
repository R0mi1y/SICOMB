from django.db import models

# Create your models here.

class Load(models.Model):
    id = models.IntegerField('Id',  primary_key=True)
    description = models.CharField('Descrição', max_length=100)
    serial_number = models.CharField('Numero de série', max_length=100)
    type_equipment = models.CharField('Tipo', max_length=50)
    caliber = models.CharField('Calibre', max_length=10)
    quantity = models.IntegerField('Quantidade')
    size = models.CharField('Tamanho', max_length=3)
    note = models.TextField('Observação', max_length=250)