from django.db import models

# Create your models here.

class equipment(models.Model):
    serial_number = models.IntegerField()
    
    name = models.CharField('Nome', max_length=250)
    uid = models.CharField('UID', max_length=100, primary_key=True) # chave primária do equipamento
    description = models.CharField('Descrição', max_length=500)
    image_path = models.TextField('caminho da imagem')
    caliber = models.CharField('Calibre', max_length=10)
    
    def __str__(self):
        return f"equipamento {self.name}"
    
    class Meta:
        verbose_name = 'Equipamento'
        ordering = ['name']