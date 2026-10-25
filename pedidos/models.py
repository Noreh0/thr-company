from decimal import Decimal

from django.conf import settings
from django.db import models

from produtos.models import Variacao


class Pedido(models.Model):
    class Status(models.TextChoices):
        AGUARDANDO = 'aguardando', 'Aguardando pagamento'
        PAGO = 'pago', 'Pago'
        ENVIADO = 'enviado', 'Enviado'
        CANCELADO = 'cancelado', 'Cancelado'

    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name='pedidos')
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.AGUARDANDO)
    total = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'))
    observacao = models.TextField(blank=True)
    criado_em = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-criado_em']

    def __str__(self):
        return f"Pedido #{self.pk} - {self.usuario}"


class ItemPedido(models.Model):
    pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE, related_name='itens')
    variacao = models.ForeignKey(Variacao, on_delete=models.SET_NULL, null=True, blank=True)
    # "Fotografia" do produto no momento da compra: não muda se o preço mudar depois.
    nome = models.CharField(max_length=150)
    tamanho = models.CharField(max_length=20)
    preco_unitario = models.DecimalField(max_digits=10, decimal_places=2)
    quantidade = models.PositiveIntegerField(default=1)

    @property
    def subtotal(self):
        return self.preco_unitario * self.quantidade

    def __str__(self):
        return f"{self.quantidade}x {self.nome} ({self.tamanho})"
