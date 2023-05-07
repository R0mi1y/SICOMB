from django.db import models

# Create your models here.

class Equipment(models.Model):
    # chave primária do equipamento
    serial_number = models.IntegerField('Numero de série')
    uid = models.CharField('UID', max_length=100, primary_key=True)
    type = models.CharField('Tipo', max_length=50)
    type_id = models.IntegerField('ID_Tipo')

    # def __str__(self):
    #     return f"Equipamento {self.name}"

    # class Meta:
    #     verbose_name = 'Equipamento'


class Armament(models.Model):
    model = models.TextField('Modelo do armamento')
    caliber = models.CharField('Calibre', max_length=10)
    description = models.CharField('Descrição', max_length=500)
    image_path = models.TextField('caminho da imagem')

    # def __str__(self):
    #     return f"Armamento"


class Wearable(models.Model):
    model = models.TextField('Modelo do armamento')
    size = models.CharField('Tamanho', max_length=10)
    description = models.CharField('Descrição', max_length=500)
    image_path = models.TextField('caminho da imagem')

    # def __str__(self):
    #     return "Vestível"