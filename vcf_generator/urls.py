# Dentro de vcf_generator/urls.py
from django.contrib import admin
from django.urls import path, include # Adicione 'include'

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('vcf_app.urls')),
    path('', include('campeonato_bt.urls')),
]