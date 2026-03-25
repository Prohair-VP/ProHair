import json
import os
from django.conf import settings

def obter_produtos():
    """
    Lê o arquivo JSON de produtos e retorna uma lista de dicionários.
    Se o arquivo não existir, retorna uma lista vazia.
    """
    # Constrói o caminho absoluto de forma segura (funciona no Linux, Windows, Mac)
    caminho_arquivo = os.path.join(settings.BASE_DIR, 'core', 'data', 'produtos.json')
    
    try:
        # Lemos o arquivo forçando o encoding utf-8 para não termos problemas com acentuação
        with open(caminho_arquivo, 'r', encoding='utf-8') as arquivo:
            produtos = json.load(arquivo)
            return produtos
    except FileNotFoundError:
        print(f"Atenção: Arquivo não encontrado em {caminho_arquivo}")
        return []
    except json.JSONDecodeError:
        print("Atenção: O arquivo JSON possui erros de formatação.")
        return []