# services.py — Camada de serviço usando Django ORM
from core.models import Produto


def obter_produtos(filtros=None):
    """
    Retorna queryset de produtos. Aceita dicionário de filtros opcionais.
    Exemplo: {'categoria': 'Banana e mel', 'q': 'shampoo'}
    """
    qs = Produto.objects.all()

    if filtros:
        busca = filtros.get('q', '').strip()
        categoria = filtros.get('categoria', '').strip()

        if busca:
            qs = qs.filter(nome_produto__icontains=busca) | qs.filter(sku__icontains=busca)

        if categoria:
            qs = qs.filter(categoria=categoria)

    return qs


def obter_categorias():
    """
    Retorna lista de categorias únicas, ordenadas alfabeticamente.
    """
    return (
        Produto.objects
        .values_list('categoria', flat=True)
        .distinct()
        .order_by('categoria')
    )


def salvar_novo_produto(dados):
    """
    Cria um novo produto no banco de dados.
    """
    return Produto.objects.create(**dados)


def editar_produto(sku_original, novos_dados):
    """
    Localiza um produto pelo SKU original e atualiza com os novos dados.
    Retorna True se encontrou e atualizou, False se não encontrou.
    """
    try:
        produto = Produto.objects.get(sku=sku_original)
        for campo, valor in novos_dados.items():
            setattr(produto, campo, valor)
        produto.save()
        return True
    except Produto.DoesNotExist:
        return False


def excluir_produto(sku_alvo):
    """
    Exclui um produto pelo SKU.
    Retorna True se encontrou e excluiu, False se não encontrou.
    """
    try:
        produto = Produto.objects.get(sku=sku_alvo)
        produto.delete()
        return True
    except Produto.DoesNotExist:
        return False


def excluir_produtos_em_massa(lista_skus):
    """
    Exclui múltiplos produtos com base em uma lista de SKUs.
    """
    if lista_skus and isinstance(lista_skus, list):
        # A exclusão em massa no Django retorna uma tupla com a quantidade deletada e um dict
        qtd, _ = Produto.objects.filter(sku__in=lista_skus).delete()
        return qtd
    return 0


def limpar_moeda(valor_string):
    """
    Converte string no formato brasileiro (1.234,56) para float.
    """
    try:
        return float(valor_string.replace('.', '').replace(',', '.'))
    except (ValueError, AttributeError):
        return 0.0


def calcular_metricas_shopee(preco_venda, preco_custo, percentual_interno_custom=35.0, frete_extra=0.0):
    """
    Calcula taxas e lucro para um produto na Shopee.
    Aceita percentual interno customizado e frete extra.
    Retorna dict com total_taxas, lucro_reais e margem_percentual.
    """
    if not preco_venda or preco_venda <= 0:
        return {"total_taxas": 0, "lucro_reais": 0, "margem_percentual": 0}

    # 1. Taxas Internas Fixas (Customizável pelo usuário, default 35%)
    percentual_interno = percentual_interno_custom / 100.0

    # 2. Regra de Comissão Shopee baseada na tabela
    if preco_venda <= 79.99:
        percentual_shopee = 0.20
        taxa_fixa_shopee = 4.00
    elif preco_venda <= 99.99:
        percentual_shopee = 0.14
        taxa_fixa_shopee = 16.00
    elif preco_venda <= 199.99:
        percentual_shopee = 0.14
        taxa_fixa_shopee = 20.00
    else:
        percentual_shopee = 0.14
        taxa_fixa_shopee = 26.00

    # 3. Cálculo Final
    total_percentual = percentual_interno + percentual_shopee
    total_taxas = (preco_venda * total_percentual) + taxa_fixa_shopee + frete_extra
    lucro = preco_venda - total_taxas - preco_custo

    # 4. Margem percentual
    margem = (lucro / preco_venda) * 100 if preco_venda > 0 else 0

    return {
        "total_taxas": round(total_taxas, 2),
        "lucro_reais": round(lucro, 2),
        "margem_percentual": round(margem, 1),
    }