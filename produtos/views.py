from django.shortcuts import render
from django.http import HttpRequest

def index(request):
    return render(request, 'produtos/index.html')

def produtos(request):
    return render(request, 'produtos/produtos.html')