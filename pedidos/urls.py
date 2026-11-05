from django.urls import path

from . import views

app_name = 'pedidos'

urlpatterns = [
    path('finalizar/', views.checkout, name='checkout'),
    path('meus-pedidos/', views.meus_pedidos, name='meus'),
]
