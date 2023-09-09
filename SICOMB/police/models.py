# from django.contrib.auth.models import AbstractUser
from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class Police(AbstractUser):
    matricula = models.CharField(max_length=20)
    telefone = models.CharField(max_length=20, unique=True)
    lotacao = models.CharField(max_length=50)
    posto = models.CharField(max_length=10)
    image_path = models.FileField(upload_to="policiais/%Y-%m-%d/")
    tipo = models.CharField(max_length=20, default="Police")

    class Meta:
        verbose_name = 'Policial'
        verbose_name_plural = 'Policiais'
        
    def __str__(self):
        return self.matricula
        