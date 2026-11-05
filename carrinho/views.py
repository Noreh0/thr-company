from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.utils.http import url_has_allowed_host_and_scheme
from django.views.decorators.http import require_POST

from produtos.models import Variacao

from .services import Carrinho


def _voltar(request, padrao='produtos:lista'):
    """Volta para a página de onde veio (só se for do próprio site)."""
    origem = request.META.get('HTTP_REFERER', '')
    if origem and url_has_allowed_host_and_scheme(origem, {request.get_host()}, request.is_secure()):
        return redirect(origem)
    return redirect(padrao)


def _inteiro(valor, padrao=None):
    try:
        return int(valor)
    except (TypeError, ValueError):
        return padrao


def ver(request):
    linhas = Carrinho(request).linhas()
    total = sum(linha.subtotal for linha in linhas)
    return render(request, 'carrinho/carrinho.html', {'linhas': linhas, 'total': total})


@require_POST
def adicionar(request):
    variacao_id = _inteiro(request.POST.get('variacao'))
    if variacao_id is None:
        messages.error(request, 'Escolha um tamanho antes de adicionar ao carrinho.')
        return _voltar(request)

    variacao = get_object_or_404(Variacao.objects.select_related('produto'), pk=variacao_id, produto__ativo=True)
    if variacao.estoque <= 0:
        messages.error(request, f'O tamanho {variacao.tamanho} está esgotado.')
        return _voltar(request)

    carrinho = Carrinho(request)
    quantidade = max(1, _inteiro(request.POST.get('quantidade'), 1))
    desejada = carrinho.quantidade_de(variacao.id) + quantidade
    if desejada > variacao.estoque:
        desejada = variacao.estoque
        messages.warning(request, f'Só temos {variacao.estoque} unidade(s) do tamanho {variacao.tamanho}. Ajustamos o carrinho.')
    else:
        messages.success(request, f'{variacao.produto.nome} ({variacao.tamanho}) foi para o carrinho.')
    carrinho.definir(variacao.id, desejada)
    return redirect('carrinho:ver')


@require_POST
def atualizar(request):
    variacao = get_object_or_404(Variacao, pk=_inteiro(request.POST.get('variacao'), 0))
    quantidade = _inteiro(request.POST.get('quantidade'), 1)
    if quantidade > variacao.estoque:
        quantidade = variacao.estoque
        messages.warning(request, f'Só temos {variacao.estoque} unidade(s) desse tamanho.')
    Carrinho(request).definir(variacao.id, quantidade)
    return redirect('carrinho:ver')


@require_POST
def remover(request):
    Carrinho(request).remover(_inteiro(request.POST.get('variacao'), 0))
    return redirect('carrinho:ver')
