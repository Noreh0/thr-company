from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import Usuario


@admin.register(Usuario)
class UsuarioAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (('Contato', {'fields': ('telefone',)}),)
    add_fieldsets = UserAdmin.add_fieldsets + (('Contato', {'fields': ('email', 'telefone')}),)
