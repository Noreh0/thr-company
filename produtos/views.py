from django.core.paginator import Paginator
from django.db.models import Count, Q
from django.shortcuts import get_object_or_404, render

from .models import Categoria, Produto


def _categorias_com_produtos():
    return (
        Categoria.objects
        .annotate(total=Count('produtos', filter=Q(produtos__ativo=True)))
        .filter(total__gt=0)
    )


def index(request):
    novidades = Produto.objects.filter(ativo=True).select_related('categoria')[:8]
    return render(request, 'produtos/index.html', {
        'novidades': novidades,
        'categorias': _categorias_com_produtos(),
    })


def produtos(request):
    lista = Produto.objects.filter(ativo=True).select_related('categoria')

    slug = request.GET.get('categoria', '')
    categoria = Categoria.objects.filter(slug=slug).first() if slug else None
    if categoria:
        lista = lista.filter(categoria=categoria)

    busca = request.GET.get('q', '').strip()
    if busca:
        lista = lista.filter(nome__icontains=busca)

    pagina = Paginator(lista, 12).get_page(request.GET.get('page'))
    return render(request, 'produtos/produtos.html', {
        'pagina': pagina,
        'categorias': _categorias_com_produtos(),
        'categoria_atual': categoria,
        'busca': busca,
    })


def detalhe(request, slug):
    produto = get_object_or_404(
        Produto.objects.select_related('categoria').prefetch_related('variacoes'),
        slug=slug, ativo=True,
    )
    variacoes = list(produto.variacoes.all())
    return render(request, 'produtos/detalhe.html', {
        'produto': produto,
        'variacoes': variacoes,
        'disponivel': any(v.estoque > 0 for v in variacoes),
    })
