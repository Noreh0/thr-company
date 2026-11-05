from django.conf import settings


def loja(request):
    """Variáveis disponíveis em todos os templates."""
    itens = request.session.get('carrinho', {})
    return {
        'carrinho_qtd': sum(itens.values()),
        'whatsapp_loja': settings.WHATSAPP_LOJA,
    }
