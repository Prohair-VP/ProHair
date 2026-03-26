from django.db import models

class Produto(models.Model):
    sku = models.CharField(max_length=20, unique=True)
    nome_produto = models.CharField(max_length=200)
    categoria = models.CharField(max_length=100)
    preco_custo = models.DecimalField(max_digits=10, decimal_places=2)
    preco_shopee = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    preco_promocional = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    # Dados de dimensão que já existem no JSON
    peso_bruto = models.DecimalField(max_digits=6, decimal_places=2, default=0)
    comprimento_cm = models.DecimalField(max_digits=6, decimal_places=2, default=0)
    largura_cm = models.DecimalField(max_digits=6, decimal_places=2, default=0)
    altura_cm = models.DecimalField(max_digits=6, decimal_places=2, default=0)
