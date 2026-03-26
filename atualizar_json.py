import json
import os

# Caminho para o banco de dados JSON da Prohair
caminho_arquivo = os.path.join('core', 'data', 'produtos.json')

def atualizar_banco_produtos():
    if not os.path.exists(caminho_arquivo):
        print("Arquivo JSON não encontrado. Verifique o caminho.")
        return

    # 1. Abre o catálogo atual
    with open(caminho_arquivo, 'r', encoding='utf-8') as f:
        produtos = json.load(f)

    contagem = 0
    # 2. Varre todos os produtos e adiciona os novos campos se não existirem
    for produto in produtos:
        modificado = False
        
        if 'preco_shopee' not in produto:
            produto['preco_shopee'] = 0.0
            modificado = True
            
        if 'preco_promocional' not in produto:
            produto['preco_promocional'] = 0.0
            modificado = True
            
        if modificado:
            contagem += 1

    # 3. Salva o catálogo atualizado
    with open(caminho_arquivo, 'w', encoding='utf-8') as f:
        json.dump(produtos, f, indent=4, ensure_ascii=False)

    print(f"Sucesso Total! {contagem} produtos receberam os campos de preço da Shopee.")

if __name__ == "__main__":
    atualizar_banco_produtos()