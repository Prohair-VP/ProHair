# views.py
from django.shortcuts import render, redirect
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from .services import (
    obter_produtos, obter_categorias, salvar_novo_produto,
    editar_produto, excluir_produto, limpar_moeda, calcular_metricas_shopee
)


@login_required
def produtos_view(request):
    # --- BLOCO ÚNICO DE PROCESSAMENTO (POST) ---
    if request.method == 'POST':
        action = request.POST.get('action')
        sku_original = request.POST.get('sku_original')

        if action == 'delete':
            if excluir_produto(sku_original):
                return redirect('produtos')

        sku_atual = request.POST.get('sku', '').strip()
        nome = request.POST.get('nome_produto', '').strip()
        categoria = request.POST.get('categoria', '').strip()
        preco_final = limpar_moeda(request.POST.get('preco_custo', '0'))

        dados_produto = {
            "sku": sku_atual,
            "nome_produto": nome,
            "categoria": categoria,
            "preco_custo": preco_final,
        }

        if action == 'edit':
            editar_produto(sku_original, dados_produto)
        else:
            salvar_novo_produto(dados_produto)

        return redirect('produtos')

    # --- BLOCO DE LISTAGEM (GET) ---
    marketplace_slug = request.GET.get('mkt', 'todos')

    if marketplace_slug == 'todos':
        marketplace_nome = 'Produtos'
    else:
        marketplace_nome = marketplace_slug.replace('_', ' ').title()

    # Filtros via query string
    filtros = {
        'q': request.GET.get('q', ''),
        'categoria': request.GET.get('categoria', ''),
    }

    lista_de_produtos = obter_produtos(filtros)
    todas_categorias = obter_categorias()

    # Paginação
    itens_por_pagina = request.GET.get('per_page', 10)
    try:
        itens_por_pagina = int(itens_por_pagina)
        if itens_por_pagina not in [10, 25, 50]:
            itens_por_pagina = 10
    except ValueError:
        itens_por_pagina = 10

    paginator = Paginator(lista_de_produtos, itens_por_pagina)
    numero_da_pagina = request.GET.get('page', 1)
    page_obj = paginator.get_page(numero_da_pagina)

    pagina_atual = page_obj.number
    total_paginas = paginator.num_pages
    start_page = max(pagina_atual - 1, 1)
    end_page = min(pagina_atual + 1, total_paginas)

    if pagina_atual == 1 and total_paginas >= 3:
        end_page = 3
    elif pagina_atual == total_paginas and total_paginas >= 3:
        start_page = total_paginas - 2

    page_range = range(start_page, end_page + 1)

    contexto = {
        'page_obj': page_obj,
        'per_page': itens_por_pagina,
        'page_range': page_range,
        'search_query': filtros['q'],
        'categorias': todas_categorias,
        'categoria_selecionada': filtros['categoria'],
        'marketplace_nome': marketplace_nome,
        'mkt': marketplace_slug,
    }

    return render(request, 'produtos.html', contexto)


@login_required
def shopee_view(request):
    # --- BLOCO DE PROCESSAMENTO (POST) ---
    if request.method == 'POST':
        action = request.POST.get('action')
        sku_original = request.POST.get('sku_original')

        sku_atual = request.POST.get('sku', '').strip()
        nome = request.POST.get('nome_produto', '').strip()
        categoria = request.POST.get('categoria', '').strip()
        preco_custo = limpar_moeda(request.POST.get('preco_custo', '0'))
        preco_shopee = limpar_moeda(request.POST.get('preco_shopee', '0'))
        preco_promo = limpar_moeda(request.POST.get('preco_promocional', '0'))

        dados_novos = {
            "sku": sku_atual,
            "nome_produto": nome,
            "categoria": categoria,
            "preco_custo": preco_custo,
            "preco_shopee": preco_shopee,
            "preco_promocional": preco_promo,
        }

        if action == 'edit':
            editar_produto(sku_original, dados_novos)

        return redirect('shopee')

    # --- BLOCO DE LISTAGEM (GET) ---
    
    # Filtros via query string
    filtros = {
        'q': request.GET.get('q', ''),
        'categoria': request.GET.get('categoria', ''),
    }

    # Parâmetros customizáveis do simulador
    tx_interna_str = request.GET.get('tx_interna', '35.0')
    frete_str = request.GET.get('frete', '0.0')
    
    try:
        tx_interna = float(tx_interna_str.replace(',', '.'))
    except (ValueError, TypeError):
        tx_interna = 35.0
        
    try:
        frete = float(frete_str.replace(',', '.'))
    except (ValueError, TypeError):
        frete = 0.0

    lista_de_produtos = obter_produtos(filtros)
    todas_categorias = obter_categorias()

    # Criamos uma lista de dicts enriquecidos com as métricas
    produtos_com_metricas = []
    for p in lista_de_produtos:
        dados = {
            'sku': p.sku,
            'nome_produto': p.nome_produto,
            'categoria': p.categoria,
            'preco_custo': p.preco_custo,
            'preco_shopee': p.preco_shopee,
            'preco_promocional': p.preco_promocional,
        }
        try:
            venda_cheia = float(p.preco_shopee or 0)
            venda_promo = float(p.preco_promocional or 0)
            custo = float(p.preco_custo or 0)
            preco_efetivo = venda_promo if venda_promo > 0 else venda_cheia

            metricas = calcular_metricas_shopee(preco_efetivo, custo, tx_interna, frete)
            dados['total_taxas'] = metricas['total_taxas']
            dados['lucro_reais'] = metricas['lucro_reais']
            dados['margem_percentual'] = metricas['margem_percentual']
        except (ValueError, TypeError):
            dados['total_taxas'] = 0.0
            dados['lucro_reais'] = 0.0
            dados['margem_percentual'] = 0.0

        produtos_com_metricas.append(dados)

    # Paginação
    itens_por_pagina = request.GET.get('per_page', 10)
    try:
        itens_por_pagina = int(itens_por_pagina)
        if itens_por_pagina not in [10, 25, 50]:
            itens_por_pagina = 10
    except ValueError:
        itens_por_pagina = 10

    paginator = Paginator(produtos_com_metricas, itens_por_pagina)
    numero_da_pagina = request.GET.get('page', 1)
    page_obj = paginator.get_page(numero_da_pagina)
    
    pagina_atual = page_obj.number
    total_paginas = paginator.num_pages
    start_page = max(pagina_atual - 1, 1)
    end_page = min(pagina_atual + 1, total_paginas)

    if pagina_atual == 1 and total_paginas >= 3:
        end_page = 3
    elif pagina_atual == total_paginas and total_paginas >= 3:
        start_page = total_paginas - 2

    page_range = range(start_page, end_page + 1)

    contexto = {
        'page_obj': page_obj,
        'per_page': itens_por_pagina,
        'page_range': page_range,
        'search_query': filtros['q'],
        'categorias': todas_categorias,
        'categoria_selecionada': filtros['categoria'],
        'tx_interna_atual': f"{tx_interna:.1f}".replace('.', ','),
        'frete_atual': f"{frete:.2f}".replace('.', ','),
        'marketplace_nome': 'Shopee Official',
    }
    return render(request, 'shopee.html', contexto)