from django.db import models

# Create your models here.
class ANALISE(models.Model):
    RENDA = models.DecimalField(max_digits=10, decimal_places=2)
    IDADE = models.IntegerField(null=True)
    EMPRESTIMO = models.DecimalField(max_digits=10, decimal_places=2)
    RESULTADO = models.IntegerField(null=True)
