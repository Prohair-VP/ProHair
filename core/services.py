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
    
def salvar_novo_produto(dados_produto):
    # 1. Define o caminho da pasta e do arquivo
    pasta_data = os.path.join(settings.BASE_DIR, 'core', 'data')
    caminho_arquivo = os.path.join(pasta_data, 'produtos.json')
    
    # 2. Segurança: Se a pasta 'data' não existir, o Python cria ela agora
    if not os.path.exists(pasta_data):
        os.makedirs(pasta_data)

    # 3. Tenta carregar os produtos atuais
    produtos = []
    if os.path.exists(caminho_arquivo):
        try:
            with open(caminho_arquivo, 'r', encoding='utf-8') as arquivo:
                produtos = json.load(arquivo)
        except json.JSONDecodeError:
            # Se o arquivo estiver corrompido ou vazio, começamos do zero
            produtos = []

    # 4. Adiciona o novo item
    produtos.append(dados_produto)
    
    # 5. Salva no arquivo
    try:
        with open(caminho_arquivo, 'w', encoding='utf-8') as arquivo:
            json.dump(produtos, arquivo, indent=4, ensure_ascii=False)
        return True
    except Exception as e:
        print(f"Erro fatal ao escrever no JSON: {e}")
        return False
    
def editar_produto_json(sku_original, novos_dados):
    """
    Localiza um produto pelo SKU original e substitui pelos novos dados no arquivo JSON.
    """
    caminho_arquivo = os.path.join(settings.BASE_DIR, 'core', 'data', 'produtos.json')
    
    # 1. Carregamos a lista atual
    with open(caminho_arquivo, 'r', encoding='utf-8') as arquivo:
        produtos = json.load(arquivo)

    # 2. Procuramos o índice do produto que queremos editar
    sucesso = False
    for i, produto in enumerate(produtos):
        if produto['sku'] == sku_original:
            # 3. Atualizamos mantendo campos que não estão no formulário (como peso e medidas)
            produtos[i].update(novos_dados)
            sucesso = True
            break
            
    # 4. Se encontramos, salvamos o arquivo inteiro de volta
    if sucesso:
        with open(caminho_arquivo, 'w', encoding='utf-8') as arquivo:
            json.dump(produtos, arquivo, indent=4, ensure_ascii=False)
            
    return sucesso

def excluir_produto_json(sku_alvo):
    # 1. Localiza o arquivo corretamente
    caminho_arquivo = os.path.join(settings.BASE_DIR, 'core', 'data', 'produtos.json')
    
    # 2. Abre e lê a lista atual
    with open(caminho_arquivo, 'r', encoding='utf-8') as arquivo:
        produtos = json.load(arquivo)
    
    # 3. Cria uma nova lista EXCLUINDO o SKU alvo (ex: 1010003 do Shampoo Banana e Mel)
    nova_lista = [p for p in produtos if p['sku'] != sku_alvo]
    
    # 4. Salva a lista limpa de volta no arquivo
    try:
        with open(caminho_arquivo, 'w', encoding='utf-8') as arquivo:
            json.dump(nova_lista, arquivo, indent=4, ensure_ascii=False)
        return True
    except Exception as e:
        print(f"Erro ao deletar: {e}")
        return False