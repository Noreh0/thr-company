from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('admin/', admin.site.urls),
    path('contas/', include('usuarios.urls')),
    path('carrinho/', include('carrinho.urls')),
    path('pedidos/', include('pedidos.urls')),
    path('', include('produtos.urls')),
]

# Em desenvolvimento, o Django serve as fotos enviadas pelo admin.
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
