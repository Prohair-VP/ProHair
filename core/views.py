from django.shortcuts import render
from django.core.paginator import Paginator
from .services import obter_produtos

def produtos_view(request):
    lista_de_produtos = obter_produtos()
    
    # 1. Extraímos todas as categorias únicas do JSON completo para o filtro
    # Usamos set() para não repetir e sorted() para ficar em ordem alfabética
    todas_categorias = sorted(list(set(p.get('categoria') for p in lista_de_produtos if p.get('categoria'))))

    # 2. Capturamos os filtros da URL
    search_query = request.GET.get('q', '').strip()
    categoria_filtrada = request.GET.get('categoria', '').strip()
    
    # 3. Lógica de Filtragem Dupla (Nome E Categoria)
    if search_query:
        lista_de_produtos = [
            p for p in lista_de_produtos 
            if search_query.lower() in p.get('nome_produto', '').lower()
        ]
        
    if categoria_filtrada:
        lista_de_produtos = [
            p for p in lista_de_produtos 
            if p.get('categoria') == categoria_filtrada
        ]

    # --- (Lógica de Paginação e Itens por Página mantida abaixo) ---
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
    
    # Lógica da Janela Deslizante (Mantida)
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
        'search_query': search_query,
        'categorias': todas_categorias, # Enviamos a lista para o select
        'categoria_selecionada': categoria_filtrada, # Para manter o select marcado
    }
    
    return render(request, 'produtos.html', contexto)