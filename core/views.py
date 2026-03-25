from django.shortcuts import render, redirect # 1. Importamos o redirect
from django.core.paginator import Paginator
from .services import obter_produtos, salvar_novo_produto # 2. Importamos a função de salvar

def produtos_view(request):
    if request.method == 'POST':
        # Captura os valores com segurança (.get com fallback vazio)
        sku = request.POST.get('sku', '').strip()
        nome = request.POST.get('nome_produto', '').strip()
        categoria = request.POST.get('categoria', '').strip()
        preco_raw = request.POST.get('preco_custo', '0')

        # Tratamento de erro para o preço (essencial para itens como o de Banana e Mel)
        try:
            # Remove pontos de milhar, troca vírgula por ponto e converte
            preco_limpo = preco_raw.replace('.', '').replace(',', '.')
            preco_final = float(preco_limpo)
        except ValueError:
            preco_final = 0.0

        novo_item = {
            "sku": sku,
            "nome_produto": nome,
            "categoria": categoria,
            "preco_custo": preco_final,
            "peso_bruto": 0.0,
            "comprimento_cm": 0.0,
            "largura_cm": 0.0,
            "altura_cm": 0.0
        }
        
        if salvar_novo_produto(novo_item):
            return redirect('produtos')
        else:
            # Se der erro no serviço, o Django não crasha, apenas segue (podemos tratar depois)
            pass
    lista_de_produtos = obter_produtos()
    
    todas_categorias = sorted(list(set(p.get('categoria') for p in lista_de_produtos if p.get('categoria'))))

    search_query = request.GET.get('q', '').strip()
    categoria_filtrada = request.GET.get('categoria', '').strip()
    
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
        'search_query': search_query,
        'categorias': todas_categorias,
        'categoria_selecionada': categoria_filtrada,
    }
    
    return render(request, 'produtos.html', contexto)