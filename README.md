# ProHair Management System 🧴✨

Este é o sistema interno de gestão da **ProHair**, desenvolvido para modernizar o controle de estoque, precificação e análise de lucratividade em marketplaces (especialmente Shopee). O sistema migrou de uma arquitetura baseada em arquivos JSON para um banco de dados relacional robusto usando **Django ORM** e **SQLite**.

---

## 🚀 Tecnologias Utilizadas

- **Backend:** Python 3.x + Django 5.x (ORM, Autenticação, Templating)
- **Banco de Dados:** SQLite (leve, rápido e embutido)
- **Frontend:** 
    - **Tailwind CSS:** Design moderno, responsivo e com tema *Dark Premium*.
    - **Alpine.js:** Reatividade leve para modais, seleções em massa e estados da UI.
    - **Google Material Symbols:** Iconografia limpa e intuitiva.

---

## 🛠️ Principais Funcionalidades

### 1. Dashboard (BI)
- Visão geral com KPIs principais: Total de produtos, categorias ativas e lucro médio.
- Gráficos e tabelas de acesso rápido.

### 2. Calculadora Shopee (O Coração do Sistema) 💸
- **Cálculo de Margem Real:** Analisa preço de custo, preço de venda, taxas de marketplace (fixas e percentuais), frete e custos operacionais.
- **Alertas Visuais:** As margens são coloridas automaticamente:
    - 🔴 **Crítico (≤ 25%)**: Alerta de baixa lucratividade.
    - 🟡 **Atenção (26% - 35%)**: Margem intermediária.
    - 🟢 **Saudável (≥ 36%)**: Margem ideal.
- **Filtros Avançados:** Busca por nome/SKU, filtragem por Categorias (Linhas) e um filtro inteligente por **Tipo de Produto** (Shampoo, Condicionador, etc.) baseado em palavras-chave no nome.

### 3. Ações em Massa ⚡
- **Exclusão em Massa:** Selecione múltiplos produtos e remova-os de uma vez.
- **Edição de Preços em Massa:** Atualize o Preço Shopee e o Preço Promocional de vários SKUs simultaneamente através de um modal intuitivo.

### 4. Gestão de Catálogo (CRUD)
- Adição, edição e exclusão de produtos com persistência de estado (ao salvar, você volta para a mesma página/filtro onde estava).

---

## 📂 Estrutura do Projeto

```text
ProHair/
├── core/                   # Aplicativo principal do Django
│   ├── models.py           # Model 'Produto' (SKU, Nome, Custo, Preços Shopee)
│   ├── services.py         # Camada de lógica (Cálculos matemáticos e Queries ORM)
│   ├── views.py            # Controladores das páginas e interceptação de POST
│   ├── templates/          # Arquivos HTML (index, produtos, shopee)
│   └── static/             # Arquivos CSS/JS (se houver, a maioria é via CDN)
├── setup/                  # Configurações do projeto (settings.py, urls.py)
├── .env                    # Variáveis de ambiente (SECRET_KEY)
├── db.sqlite3              # Banco de dados local
├── requirements.txt        # Dependências do Python
└── migrar_json.py          # Script utilitário para importar dados legados
```

---

## ⚙️ Como Rodar o Projeto (Guia do Desenvolvedor)

1. **Instale as dependências:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Configure o Ambiente:**
   Certifique-se de que o arquivo `.env` exista na raiz com a variável `SECRET_KEY`.

3. **Migrações e Banco:**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

4. **Crie um Usuário (Admin):**
   ```bash
   python manage.py createsuperuser
   ```

5. **Inicie o Servidor:**
   ```bash
   python manage.py runserver
   ```
   Acesse em: `http://127.0.0.1:8000`

---

## 📝 Notas de Manutenção

- **Cálculos de Taxas:** Toda a lógica matemática da Shopee está centralizada em `core/services.py` na função `calcular_metricas_shopee`. Se as regras da Shopee mudarem, este é o único lugar que precisa de alteração.
- **Filtros de Tipo:** O filtro por tipo (Shampoo, etc.) em `services.py` usa `Q objects` do Django para buscar variações de nomes. Se precisar adicionar novos tipos, basta incluir uma nova cláusula `elif` na função `obter_produtos`.
- **Alpine.js:** Os estados de seleção em massa (checkboxes) e controle de modais estão embutidos diretamente nos arquivos HTML dentro do atributo `x-data`.

---

**Desenvolvido para ProHair — Modernizando a beleza com tecnologia.** 🚀💇‍♀️
