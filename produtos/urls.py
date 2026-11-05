from django.urls import path

from . import views

app_name = 'produtos'

urlpatterns = [
    path('', views.index, name='home'),
    path('produtos/', views.produtos, name='lista'),
    path('produtos/<slug:slug>/', views.detalhe, name='detalhe'),
]
