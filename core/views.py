# views.py
from django.shortcuts import render, redirect
from django.core.paginator import Paginator
from .services import obter_produtos, salvar_novo_produto, editar_produto_json, excluir_produto_json

def produtos_view(request):
    # --- BLOCO ÚNICO DE PROCESSAMENTO (POST) ---
    if request.method == 'POST':
        action = request.POST.get('action')
        sku_original = request.POST.get('sku_original')
        
        if action == 'delete':
            if excluir_produto_json(sku_original):
                return redirect('produtos')

        sku_atual = request.POST.get('sku', '').strip()
        nome = request.POST.get('nome_produto', '').strip()
        categoria = request.POST.get('categoria', '').strip()
        preco_raw = request.POST.get('preco_custo', '0')

        try:
            preco_limpo = preco_raw.replace('.', '').replace(',', '.')
            preco_final = float(preco_limpo)
        except ValueError:
            preco_final = 0.0

        dados_produto = {
            "sku": sku_atual,
            "nome_produto": nome,
            "categoria": categoria,
            "preco_custo": preco_final,
            "peso_bruto": 0.0,
            "comprimento_cm": 0.0,
            "largura_cm": 0.0,
            "altura_cm": 0.0
        }

        if action == 'edit':
            editar_produto_json(sku_original, dados_produto)
        else:
            salvar_novo_produto(dados_produto)

        return redirect('produtos')
    
    # --- BLOCO DE LISTAGEM (GET) ---
    lista_de_produtos = obter_produtos()
    
    # 1. CAPTURA O MARKETPLACE DA URL
    marketplace_slug = request.GET.get('mkt', 'todos')
    
    # Converte o slug (ex: mercado_livre) para um nome bonito (Mercado Livre)
    if marketplace_slug == 'todos':
        marketplace_nome = 'Produtos'
    else:
        marketplace_nome = marketplace_slug.replace('_', ' ').title()

    todas_categorias = sorted(list(set(p.get('categoria') for p in lista_de_produtos if p.get('categoria'))))

    search_query = request.GET.get('q', '').strip()
    categoria_filtrada = request.GET.get('categoria', '').strip()
    
    if search_query:
        query = search_query.lower()
        lista_de_produtos = [
            p for p in lista_de_produtos 
            if query in p.get('nome_produto', '').lower() or 
            query in str(p.get('sku', '')).lower()
        ]
        
    if categoria_filtrada:
        lista_de_produtos = [
            p for p in lista_de_produtos 
            if p.get('categoria') == categoria_filtrada
        ]

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
    
    # 2. ADICIONA O NOME DO MARKETPLACE AO CONTEXTO
    contexto = {
        'page_obj': page_obj,
        'per_page': itens_por_pagina,
        'page_range': page_range,
        'search_query': search_query,
        'categorias': todas_categorias,
        'categoria_selecionada': categoria_filtrada,
        'marketplace_nome': marketplace_nome, # Nome que aparecerá no título
        'mkt': marketplace_slug # Slug para manter o filtro nas próximas páginas
    }
    
    return render(request, 'produtos.html', contexto)

def shopee_view(request):
    lista_de_produtos = obter_produtos()
    paginator = Paginator(lista_de_produtos, 10)
    page_obj = paginator.get_page(request.GET.get('page', 1))

    contexto = {
        'page_obj': page_obj,
        'marketplace_nome': 'Shopee Official',
        'cor_destaque': 'orange-500',
    }
    return render(request, 'shopee.html', contexto)