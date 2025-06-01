# Dentro de vcf_generator/urls.py
from django.contrib import admin
from django.urls import path, include # Adicione 'include'

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('vcf_app.urls')), # Ou apenas path('', include('vcf_app.urls')) se quiser na raiz do site
]