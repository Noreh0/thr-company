from decimal import Decimal

from produtos.models import Variacao

SESSION_KEY = 'carrinho'


class Carrinho:
    """Carrinho guardado na sessão: {variacao_id: quantidade}. Não tem tabela."""

    def __init__(self, request):
        self.session = request.session
        self.itens = self.session.setdefault(SESSION_KEY, {})

    def adicionar(self, variacao_id, quantidade=1):
        chave = str(variacao_id)
        self.itens[chave] = self.itens.get(chave, 0) + quantidade
        self._salvar()

    def remover(self, variacao_id):
        self.itens.pop(str(variacao_id), None)
        self._salvar()

    def limpar(self):
        self.session[SESSION_KEY] = {}
        self.itens = self.session[SESSION_KEY]
        self.session.modified = True

    def linhas(self):
        """Devolve (variacao, quantidade, subtotal) lendo preço do BANCO."""
        variacoes = Variacao.objects.select_related('produto').in_bulk(int(k) for k in self.itens)
        resultado = []
        for chave, qtd in self.itens.items():
            v = variacoes.get(int(chave))
            if v and v.produto.ativo:
                resultado.append((v, qtd, v.produto.preco * qtd))
        return resultado

    def total(self):
        return sum((sub for _, _, sub in self.linhas()), Decimal('0.00'))

    def _salvar(self):
        self.session.modified = True
