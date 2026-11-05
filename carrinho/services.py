from decimal import Decimal
from typing import NamedTuple

from produtos.models import Variacao

SESSION_KEY = 'carrinho'


class Linha(NamedTuple):
    variacao: Variacao
    quantidade: int
    subtotal: Decimal

    @property
    def produto(self):
        return self.variacao.produto


class Carrinho:
    """Carrinho guardado na sessão: {variacao_id: quantidade}. Não tem tabela,
    então visitantes sem login também podem montar o carrinho."""

    def __init__(self, request):
        self.session = request.session
        self.itens = self.session.setdefault(SESSION_KEY, {})

    def quantidade_de(self, variacao_id):
        return self.itens.get(str(variacao_id), 0)

    def definir(self, variacao_id, quantidade):
        """Define a quantidade; zero ou menos remove o item."""
        if quantidade <= 0:
            self.itens.pop(str(variacao_id), None)
        else:
            self.itens[str(variacao_id)] = quantidade
        self.session.modified = True

    def remover(self, variacao_id):
        self.definir(variacao_id, 0)

    def limpar(self):
        self.session[SESSION_KEY] = {}
        self.itens = self.session[SESSION_KEY]
        self.session.modified = True

    def linhas(self):
        """Linhas do carrinho com o preço lido do BANCO (nunca do navegador).
        Itens inativos ou sem estoque somem; quantidades acima do estoque
        são reduzidas ao que existe."""
        ids = [int(k) for k in self.itens]
        variacoes = Variacao.objects.select_related('produto').in_bulk(ids)
        resultado = []
        for chave, qtd in self.itens.items():
            v = variacoes.get(int(chave))
            if not v or not v.produto.ativo or v.estoque <= 0:
                continue
            qtd = min(qtd, v.estoque)
            resultado.append(Linha(v, qtd, v.produto.preco * qtd))
        return resultado

    def total(self):
        return sum((linha.subtotal for linha in self.linhas()), Decimal('0.00'))
