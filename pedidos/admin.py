from django.contrib import admin
from django.utils.html import format_html

from .models import ItemPedido, Pedido
from .services import devolver_estoque


class ItemPedidoInline(admin.TabularInline):
    model = ItemPedido
    extra = 0
    fields = ('nome', 'tamanho', 'preco_unitario', 'quantidade')
    readonly_fields = fields
    can_delete = False

    def has_add_permission(self, request, obj=None):
        return False


@admin.register(Pedido)
class PedidoAdmin(admin.ModelAdmin):
    list_display = ('id', 'usuario', 'whatsapp_cliente', 'total', 'status', 'criado_em')
    list_editable = ('status',)
    list_filter = ('status',)
    search_fields = ('usuario__first_name', 'usuario__email', 'usuario__telefone')
    readonly_fields = ('usuario', 'total', 'criado_em', 'estoque_devolvido')
    inlines = [ItemPedidoInline]

    @admin.display(description='WhatsApp do cliente')
    def whatsapp_cliente(self, pedido):
        tel = pedido.usuario.telefone
        return format_html('<a href="https://wa.me/55{}" target="_blank" rel="noopener">{}</a>', tel, tel)

    def save_model(self, request, obj, form, change):
        cancelou = change and 'status' in form.changed_data and obj.status == Pedido.Status.CANCELADO
        super().save_model(request, obj, form, change)
        if cancelou:
            devolver_estoque(obj)
