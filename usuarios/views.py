from django.contrib import messages
from django.contrib.auth import login
from django.shortcuts import redirect, render
from django.utils.http import url_has_allowed_host_and_scheme

from .forms import CadastroForm


def _destino(request):
    url = request.POST.get('next') or request.GET.get('next') or ''
    if url and url_has_allowed_host_and_scheme(url, {request.get_host()}, request.is_secure()):
        return url
    return 'produtos:home'


def cadastro(request):
    if request.user.is_authenticated:
        return redirect('produtos:home')
    destino = _destino(request)
    form = CadastroForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        usuario = form.save()
        login(request, usuario)
        messages.success(request, f'Conta criada. Bem-vindo, {usuario.first_name}!')
        return redirect(destino)
    return render(request, 'usuarios/cadastro.html', {
        'form': form,
        'next': request.POST.get('next') or request.GET.get('next') or '',
    })
