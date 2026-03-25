import json
import os

# Caminho para o seu arquivo de dados da Prohair
caminho_arquivo = os.path.join('core', 'data', 'produtos.json')

def adicionar_campo_shopee():
    if not os.path.exists(caminho_arquivo):
        print("Arquivo não encontrado!")
        return

    # 1. Lê os dados atuais
    with open(caminho_arquivo, 'r', encoding='utf-8') as f:
        produtos = json.load(f)

    # 2. Adiciona o campo em cada item
    contagem = 0
    for produto in produtos:
        if 'preco_shopee' not in produto:
            produto['preco_shopee'] = 0.0
            contagem += 1

    # 3. Salva de volta no JSON
    with open(caminho_arquivo, 'w', encoding='utf-8') as f:
        json.dump(produtos, f, indent=4, ensure_ascii=False)

    print(f"Sucesso! {contagem} produtos foram atualizados com o campo 'preco_shopee'.")

if __name__ == "__main__":
    adicionar_campo_shopee()