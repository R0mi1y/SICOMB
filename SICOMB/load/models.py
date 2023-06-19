from django.db import models
from equipment.models import Equipment, Bullet
from police.models import Police, RegisterPolice
from django.utils import timezone

# from adjunct.models import Adjunct #Para importar o modelo do Adjunto

# Create your models here.


class Load(models.Model):
    situation = models.CharField("Situação da carga", max_length=20, default="Pendente")
    date_load = models.DateTimeField(default=timezone.now)
    expected_load_return_date = models.DateTimeField("Data Prevista de Devolução", null=True)
    turn_type = models.CharField(max_length=20)
    # nomear atributo que receberá os dados: 6h, 12h, 24h, conserto, requisição judicial ou indeterminado
    status = models.CharField("horário_carga", max_length=20, default="Pendente")
    police = models.ForeignKey(RegisterPolice, on_delete=models.CASCADE)
    # adjunct = models.ForeignKey(Adjunct, on_delete=models.CASCADE) #Pega a chave primária do adjunto
    
    def __str__(self):
        return str(self.pk)


# Tabela que faz o relacionamento entre a carga e os equipamentos
class Equipment_load(models.Model):
    load = models.ForeignKey(Load, on_delete=models.CASCADE)
    equipment = models.ForeignKey(
        Equipment, on_delete=models.CASCADE, null=True, default=None
    )
    bullet = models.ForeignKey(
        Bullet, on_delete=models.CASCADE, null=True, default=None
    )
    amount = models.IntegerField("Quantidade", null=True, default="1")
    observation = models.TextField("Observação", default=None, null=True)
    status = models.CharField('Status', max_length=20, default='Aprovado')
    
    # o amount diz, caso seja uma munição, a quantidade selecionada nessa carga em específico e dessa munição em específico

