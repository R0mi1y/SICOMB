# from django.contrib.auth.models import AbstractUser
from django.db import models
from django.contrib.auth.models import AbstractUser
from SICOMB import settings

# Create your models here.

class Police(AbstractUser):
    name = models.CharField("Nome", max_length=200, unique=True)
    activator = models.ForeignKey('self', on_delete=models.DO_NOTHING, default=None, null=True)
    activated = models.BooleanField("Ativado", default=False)
    matricula = models.CharField(max_length=20)
    telefone = models.CharField(max_length=20, unique=True)
    lotacao = models.CharField(max_length=50)
    posto = models.CharField("Posto/Graduação", max_length=50, choices=settings.AUX['postos'])
    image_path = models.FileField(upload_to="policiais/%Y-%m-%d/")
    tipo = models.CharField(max_length=20, default="Police", choices=[("Policial", "Policial"), ("Adjunto","Adjunto"), ("Admin", "Admin")])
    fingerprint = models.CharField(max_length=250, null=True, default=None)

    class Meta:
        verbose_name = 'Policial'
        verbose_name_plural = 'Policiais'
        
    def __str__(self):
        return self.name
        