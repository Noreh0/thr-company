from setup.urls import urlpatterns
from django.urls import path
from produtos.views import index, produtos

urlpatterns = [
    path('', index),
    path('produtos/', produtos)
]