from urllib.parse import quote

from django.conf import settings
from django.db import transaction

from produtos.models import Variacao

from .models import ItemPedido, Pedido


class EstoqueInsuficiente(Exception):
    def __init__(self, variacao):
        self.variacao = variacao
        super().__init__(f'{variacao.produto.nome} ({variacao.tamanho}) não tem estoque suficiente.')


def brl(valor):
    """1799.8 -> 'R$ 1.799,80'"""
    texto = f'{valor:,.2f}'.replace(',', 'X').replace('.', ',').replace('X', '.')
    return f'R$ {texto}'


def formatar_telefone(digitos):
    if len(digitos) == 11:
        return f'({digitos[:2]}) {digitos[2:7]}-{digitos[7:]}'
    if len(digitos) == 10:
        return f'({digitos[:2]}) {digitos[2:6]}-{digitos[6:]}'
    return digitos


@transaction.atomic
def criar_pedido(usuario, carrinho):
    """Transforma o carrinho em Pedido, baixa o estoque e esvazia o carrinho."""
    linhas = carrinho.linhas()
    if not linhas:
        raise ValueError('Carrinho vazio')

    # Trava as variações para duas compras simultâneas não venderem a mesma peça.
    travadas = Variacao.objects.select_for_update().select_related('produto').in_bulk(
        [linha.variacao.id for linha in linhas]
    )
    for linha in linhas:
        if travadas[linha.variacao.id].estoque < linha.quantidade:
            raise EstoqueInsuficiente(linha.variacao)

    pedido = Pedido.objects.create(usuario=usuario)
    total = 0
    for linha in linhas:
        variacao = travadas[linha.variacao.id]
        ItemPedido.objects.create(
            pedido=pedido,
            variacao=variacao,
            nome=variacao.produto.nome,
            tamanho=variacao.tamanho,
            preco_unitario=variacao.produto.preco,
            quantidade=linha.quantidade,
        )
        variacao.estoque -= linha.quantidade
        variacao.save(update_fields=['estoque'])
        total += linha.subtotal
    pedido.total = total
    pedido.save(update_fields=['total'])
    carrinho.limpar()
    return pedido


@transaction.atomic
def devolver_estoque(pedido):
    """Chamado quando o pedido é cancelado. Só devolve uma vez."""
    if pedido.estoque_devolvido:
        return
    for item in pedido.itens.select_related('variacao'):
        if item.variacao:
            item.variacao.estoque += item.quantidade
            item.variacao.save(update_fields=['estoque'])
    pedido.estoque_devolvido = True
    pedido.save(update_fields=['estoque_devolvido'])


def link_whatsapp(pedido):
    """Link wa.me com a mensagem do pedido já preenchida."""
    cliente = pedido.usuario
    linhas = [
        f'Olá! Quero finalizar o pedido #{pedido.pk}.',
        '',
        f'Cliente: {cliente} - {formatar_telefone(cliente.telefone)}',
        '',
    ]
    for item in pedido.itens.all():
        linhas.append(f'- {item.quantidade}x {item.nome} ({item.tamanho}) - {brl(item.preco_unitario)}')
    linhas += ['', f'Total: {brl(pedido.total)}']
    return f'https://wa.me/{settings.WHATSAPP_LOJA}?text={quote(chr(10).join(linhas))}'
