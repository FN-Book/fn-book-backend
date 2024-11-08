from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),  # URL do painel de administração
    path('', include('core.urls')),   # Inclui as URLs do aplicativo 'core'
]
