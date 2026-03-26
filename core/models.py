from django.db import models


class Produto(models.Model):
    sku = models.CharField(max_length=20, unique=True)
    nome_produto = models.CharField(max_length=200)
    categoria = models.CharField(max_length=100)
    preco_custo = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    preco_shopee = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    preco_promocional = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    peso_bruto = models.DecimalField(max_digits=6, decimal_places=2, default=0)
    comprimento_cm = models.DecimalField(max_digits=6, decimal_places=2, default=0)
    largura_cm = models.DecimalField(max_digits=6, decimal_places=2, default=0)
    altura_cm = models.DecimalField(max_digits=6, decimal_places=2, default=0)
    # Rastreabilidade: quando o produto foi cadastrado e atualizado
    criado_em = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['nome_produto']
        verbose_name = 'Produto'
        verbose_name_plural = 'Produtos'

    def __str__(self):
        return f'{self.sku} - {self.nome_produto}'
