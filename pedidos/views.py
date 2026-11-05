from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render

from carrinho.services import Carrinho

from .models import Pedido
from .services import EstoqueInsuficiente, criar_pedido, link_whatsapp


@login_required
def checkout(request):
    carrinho = Carrinho(request)
    linhas = carrinho.linhas()
    if not linhas:
        messages.info(request, 'Seu carrinho está vazio.')
        return redirect('carrinho:ver')

    if request.method == 'POST':
        try:
            pedido = criar_pedido(request.user, carrinho)
        except EstoqueInsuficiente as erro:
            messages.error(request, f'{erro} Revise as quantidades.')
            return redirect('carrinho:ver')
        # O pedido já está salvo; agora o cliente segue para o WhatsApp da loja.
        return redirect(link_whatsapp(pedido))

    total = sum(linha.subtotal for linha in linhas)
    return render(request, 'pedidos/checkout.html', {'linhas': linhas, 'total': total})


@login_required
def meus_pedidos(request):
    pedidos = list(
        Pedido.objects.filter(usuario=request.user).select_related('usuario').prefetch_related('itens')
    )
    for pedido in pedidos:
        if pedido.status == Pedido.Status.AGUARDANDO:
            pedido.link_whatsapp = link_whatsapp(pedido)
    return render(request, 'pedidos/meus_pedidos.html', {'pedidos': pedidos})
