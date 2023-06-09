from django.db import models
from equipment.models import Equipment, Bullet
from police.models import Police, RegisterPolice
from django.utils import timezone
# from adjunct.models import Adjunct #Para importar o modelo do Adjunto

# Create your models here.

class Cargo(models.Model):
    situation = models.CharField("Devolvido", max_length=20, default="Pendente")
    date_cargo = models.DateTimeField(default=timezone.now)
    expected_cargo_return_date = models.DateTimeField('Data Prevista de Devolução')
    # nomear atributo que receberá os dados: 6h, 12h, 24h, conserto, requisição judicial ou indeterminado
    status = models.CharField("horário_carga", max_length=20, default="Pendente")
    # police = models.OneToOneField(RegisterPolice, on_delete=models.CASCADE)
    # adjunct = models.ForeignKey(Adjunct, on_delete=models.CASCADE) #Pega a chave primária do adjunto

class Equipment_cargo(models.Model):
    cargo = models.ForeignKey(Cargo, on_delete=models.DO_NOTHING)
    equipment = models.ForeignKey(Equipment, on_delete=models.DO_NOTHING)
    bullet = models.ForeignKey(Bullet, on_delete=models.CASCADE, null=True, default=None)
    bullet_amount = models.IntegerField("Quantidade_munição", null=True, default=None)