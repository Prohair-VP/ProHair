import json
import os
from django.core.management.base import BaseCommand
from django.conf import settings
from core.models import Produto


class Command(BaseCommand):
    help = 'Importa todos os produtos do arquivo produtos.json para o banco de dados SQLite'

    def handle(self, *args, **options):
        caminho = os.path.join(settings.BASE_DIR, 'core', 'data', 'produtos.json')

        with open(caminho, 'r', encoding='utf-8') as f:
            produtos_json = json.load(f)

        self.stdout.write(f'Encontrados {len(produtos_json)} produtos no JSON.')

        criados = 0
        atualizados = 0
        erros = 0

        for item in produtos_json:
            try:
                produto, foi_criado = Produto.objects.update_or_create(
                    sku=item.get('sku', ''),
                    defaults={
                        'nome_produto': item.get('nome_produto', ''),
                        'categoria': item.get('categoria', ''),
                        'preco_custo': float(item.get('preco_custo', 0) or 0),
                        'preco_shopee': float(item.get('preco_shopee', 0) or 0),
                        'preco_promocional': float(item.get('preco_promocional', 0) or 0),
                        'peso_bruto': float(item.get('peso_bruto', 0) or 0),
                        'comprimento_cm': float(item.get('comprimento_cm', 0) or 0),
                        'largura_cm': float(item.get('largura_cm', 0) or 0),
                        'altura_cm': float(item.get('altura_cm', 0) or 0),
                    }
                )
                if foi_criado:
                    criados += 1
                else:
                    atualizados += 1
            except Exception as e:
                erros += 1
                self.stderr.write(f'Erro no SKU {item.get("sku")}: {e}')

        self.stdout.write(self.style.SUCCESS(
            f'\n✅ Importação concluída!'
            f'\n   Criados: {criados}'
            f'\n   Atualizados: {atualizados}'
            f'\n   Erros: {erros}'
        ))
