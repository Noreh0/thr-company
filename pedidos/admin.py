from django.contrib import admin

from .models import ItemPedido, Pedido


class ItemPedidoInline(admin.TabularInline):
    model = ItemPedido
    extra = 0
    readonly_fields = ('nome', 'tamanho', 'preco_unitario', 'quantidade')
    can_delete = False


@admin.register(Pedido)
class PedidoAdmin(admin.ModelAdmin):
    list_display = ('id', 'usuario', 'status', 'total', 'criado_em')
    list_filter = ('status',)
    list_editable = ('status',)
    inlines = [ItemPedidoInline]
