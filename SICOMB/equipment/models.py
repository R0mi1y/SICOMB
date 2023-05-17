from django.db import models

#imagem para caso não tenha uma imagem ainda
img_alt = ''

class Equipment(models.Model):
    # chave primária do equipamento
    serial_number = models.CharField('Numero de série', max_length=20)
    uid = models.CharField('UID', max_length=20, primary_key=True)
    type = models.CharField('Tipo', max_length=50, default='Bullet')
    type_id = models.CharField('Tipo', max_length=50, default='Bullet')
    observation = models.TextField('Observação')
    status = models.CharField("Estado atual", max_length=10, default="Disponível")

    # def __str__(self):
    #     return f"Equipamento {self.name}"

    # class Meta:
    #     verbose_name = 'Equipamento'

class Model_bullet(models.Model):
    type = models.CharField('Tipo', max_length=50, default='Bullet')
    amount = models.IntegerField('Quantidade', default=0)
    image_path = models.TextField('caminho da imagem', default=img_alt)
    caliber = models.CharField('Calibre', max_length=50)


class Model_armament(models.Model):
    model = models.TextField('Modelo do armamento')
    caliber = models.CharField('Calibre', max_length=10)
    image_path = models.TextField('caminho da imagem', default=img_alt)

    # def __str__(self):
    #     return f"Armamento"


class Model_wearable(models.Model):
    model = models.TextField('Modelo do armamento')
    size = models.CharField('Tamanho', max_length=10)
    image_path = models.TextField('caminho da imagem', default=img_alt)

    # def __str__(self):
    #     return "Vestível"