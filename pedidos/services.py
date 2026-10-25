from urllib.parse import quote

from django.conf import settings
from django.db import transaction

from .models import ItemPedido, Pedido


@transaction.atomic
def criar_pedido(usuario, carrinho):
    linhas = carrinho.linhas()
    if not linhas:
        raise ValueError('Carrinho vazio')
    pedido = Pedido.objects.create(usuario=usuario)
    total = 0
    for variacao, qtd, subtotal in linhas:
        ItemPedido.objects.create(
            pedido=pedido, variacao=variacao,
            nome=variacao.produto.nome, tamanho=variacao.tamanho,
            preco_unitario=variacao.produto.preco, quantidade=qtd,
        )
        total += subtotal
    pedido.total = total
    pedido.save(update_fields=['total'])
    carrinho.limpar()
    return pedido


def link_whatsapp(pedido):
    linhas = [f"Olá! Pedido #{pedido.pk} - {pedido.usuario}"]
    for i in pedido.itens.all():
        linhas.append(f"- {i.quantidade}x {i.nome} ({i.tamanho}) R$ {i.preco_unitario}")
    linhas.append(f"Total: R$ {pedido.total}")
    return f"https://wa.me/{settings.WHATSAPP_LOJA}?text={quote(chr(10).join(linhas))}"
