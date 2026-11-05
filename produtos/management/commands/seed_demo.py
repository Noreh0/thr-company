from decimal import Decimal

from django.core.management.base import BaseCommand

from produtos.models import Categoria, Produto, Variacao

TAMANHOS_ROUPA = ['P', 'M', 'G', 'GG']
TAMANHOS_TENIS = ['39', '40', '41', '42', '43']

DEMO = {
    'Camisas': ('Camiseta', ['Oversized preta', 'Oversized branca', 'Gráfica logo', 'Manga longa'], '129.90', TAMANHOS_ROUPA, {'tipo_manga': 'curta'}),
    'Calças': ('Calça', ['Cargo preta', 'Jogger moletom', 'Jeans reta'], '249.90', ['38', '40', '42', '44'], {'tipo_modelagem': 'reta'}),
    'Blusas': ('Moletom', ['Hoodie zip preto', 'Hoodie cinza', 'Crewneck básico'], '299.90', TAMANHOS_ROUPA, {'tipo_gola': 'capuz'}),
    'Tênis': ('Tênis', ['Cano baixo', 'Cano alto'], '599.90', TAMANHOS_TENIS, {'tipo_sola': 'borracha'}),
    'Acessórios': ('Boné', ['Aba curva preto', 'Bucket'], '99.90', ['Único'], {'material': 'algodão'}),
}


class Command(BaseCommand):
    help = 'Cria categorias, produtos e variações de exemplo para testar o site (pode rodar mais de uma vez).'

    def handle(self, *args, **options):
        criados = 0
        for nome_categoria, (prefixo, modelos, preco, tamanhos, atributos) in DEMO.items():
            categoria, _ = Categoria.objects.get_or_create(nome=nome_categoria)
            for modelo in modelos:
                produto, novo = Produto.objects.get_or_create(
                    nome=f'{prefixo} {modelo}',
                    defaults={
                        'categoria': categoria,
                        'descricao': f'{prefixo} {modelo.lower()}. Produto de exemplo para testar o catálogo.',
                        'preco': Decimal(preco),
                        'atributos': atributos,
                    },
                )
                if novo:
                    criados += 1
                    for i, tamanho in enumerate(tamanhos):
                        # o último tamanho esgotado, para ver o estado "esgotado" na tela
                        Variacao.objects.create(produto=produto, tamanho=tamanho, estoque=0 if i == len(tamanhos) - 1 and len(tamanhos) > 1 else 5)
        self.stdout.write(self.style.SUCCESS(f'{criados} produtos de exemplo criados.'))
