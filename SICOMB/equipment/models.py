from django.db import models

# Create your models here.


class Equipment(models.Model):
    serial_number = models.IntegerField('Numero de série')
    # chave primária do equipamento
    uid = models.CharField('UID', max_length=100, primary_key=True)
    description = models.CharField('Descrição', max_length=500)
    image_path = models.TextField('caminho da imagem')
    type = models.CharField('Tipo', max_length=50)

    def __str__(self):
        return f"Equipamento {self.name}"

    class Meta:
        verbose_name = 'Equipamento'


class Armament(models.Model):
    equipment_uid = models.ForeignKey(Equipment, on_delete=models.CASCADE)
    model = models.TextField('Modelo do armamento')
    caliber = models.CharField('Calibre', max_length=10)

    def __str__(self):
        return f"Armamento"


class Wearable(models.Model):
    equipment_uid = models.ForeignKey(Equipment, on_delete=models.CASCADE)
    size = models.CharField('Tamanho', max_length=10)

    def __str__(self):
        return "Vestível"
    
# Modelo para preenchimento dos campos de armamento
class Armament_model(models.Model):
    description = models.CharField('Descrição', max_length=500)
    image_path = models.TextField('caminho da imagem')
    type = models.CharField('Tipo', max_length=50)
    model = models.TextField('Modelo do armamento')
    
# Modelo para preenchimento dos campos de vestíveis
class Wearble_model(models.Model):
    description = models.CharField('Descrição', max_length=500)
    image_path = models.TextField('caminho da imagem')
    type = models.CharField('Tipo', max_length=50)
    size = models.TextField('Modelo do armamento')