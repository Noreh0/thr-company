from django.contrib import admin

from .models import Categoria, Produto, Variacao


class VariacaoInline(admin.TabularInline):
    model = Variacao
    extra = 1


@admin.register(Produto)
class ProdutoAdmin(admin.ModelAdmin):
    list_display = ('nome', 'categoria', 'preco', 'ativo')
    list_filter = ('categoria', 'ativo')
    search_fields = ('nome',)
    inlines = [VariacaoInline]


admin.site.register(Categoria)
