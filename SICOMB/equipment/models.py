import datetime
from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from SICOMB import settings
from django.utils import timezone

# imagem para caso não tenha uma imagem ainda


class Model_armament(models.Model):
    activated = models.BooleanField("Ativado", default=False)
    model = models.TextField("Modelo do armamento")
    caliber = models.CharField("Calibre", choices=settings.AUX['calibres'], default="SELECIONE", max_length=30)
    description = models.TextField("Descrição")
    image_path = models.FileField(upload_to="Modelos/armamentos/")

    def __str__(self):
        # na hora dos campos do select ele retorna isso
        return f"Armamento {self.model}"


class Model_wearable(models.Model):
    activated = models.BooleanField("Ativado", default=False)
    model = models.TextField("Modelo do armamento")
    size = models.CharField("Tamanho", max_length=10)
    description = models.TextField("Descrição")
    image_path = models.FileField(upload_to="Modelos/vestiveis/")

    def __str__(self):
        # na hora dos campos do select ele retorna isso
        return f"Vestível {self.model}"


class Model_accessory(models.Model):  # bastão, escudo
    activated = models.BooleanField("Ativado", default=False)
    model = models.TextField("Modelo do armamento")
    description = models.TextField("Descrição")
    image_path = models.FileField(upload_to="Modelos/acessorios/")

    def __str__(self):
        # na hora dos campos do select ele retorna isso
        return f"Acessório {self.model}"


class Model_grenada(models.Model):
    activated = models.BooleanField("Ativado", default=False)
    model = models.TextField("Modelo do armamento")
    image_path = models.FileField(upload_to="Modelos/granadas/")
    description = models.TextField("Descrição")

    def __str__(self):
        # na hora dos campos do select ele retorna isso
        return f"Granada {self.model}"


class Equipment(models.Model):
    CHOICES = (
        ("Disponível", "Disponível"),
        ("6H", "6H"),
        ("8H", "8H"),
        ("12H", "12H"),
        ("24H", "24H"),
        ("CONSERTO", "CONSERTO"),
        ("INDETERMINADO", "INDETERMINADO"),
        ("REQUISIÇÃO JUDICIAL", "REQUISIÇÃO JUDICIAL"),
    )
    date_register = models.DateTimeField("Data de registro", default=timezone.now)
    activated = models.BooleanField("Ativado", default=False)
    serial_number = models.CharField("Numero de série", max_length=20, null=True, unique=True)
    uid = models.CharField("uid", max_length=20, primary_key=True, default=None)
    status = models.CharField("Estado atual", choices=CHOICES, max_length=20, default="Disponível")
    model_type = models.ForeignKey(ContentType, verbose_name="Tipo do modelo", on_delete=models.CASCADE)
    model_id = models.PositiveIntegerField(verbose_name="modelo")
    model = GenericForeignKey("model_type", "model_id")

    def __str__(self):
        # na hora dos campos do select ele retorna isso
        return f"Equipamento {self.uid}"

    class Meta:
        verbose_name = "Equipamento"


class Bullet(models.Model):
    activated = models.BooleanField("Ativado", default=False)
    amount = models.IntegerField("Quantidade", default=0)
    image_path = models.FileField(upload_to="Modelos/municoes/")
    caliber = models.CharField("Calibre", choices=settings.AUX['calibres'], default="SELECIONE", max_length=30)
    description = models.TextField("Descrição")

    def __str__(self):
        # na hora dos campos do select ele retorna isso
        return f"Munição {self.caliber}"
