from django.contrib import admin
from .models import Produto


@admin.register(Produto)
class ProdutoAdmin(admin.ModelAdmin):
    list_display = ('sku', 'nome_produto', 'categoria', 'preco_custo', 'preco_shopee', 'preco_promocional')
    list_filter = ('categoria',)
    search_fields = ('sku', 'nome_produto')
    list_per_page = 25
    list_editable = ('preco_custo', 'preco_shopee', 'preco_promocional')
