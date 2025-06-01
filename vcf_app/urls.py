# Dentro de vcf_app/urls.py
from django.urls import path
from . import views # Importa as views do app atual

app_name = 'vcf_app' # Boa prática para namespacing

urlpatterns = [
    path('', views.gerador_vcf_view, name='pagina_gerador_vcf'),
    # O '' significa a raiz do app, ex: se o app for em /gerador/, esta será /gerador/
    # name='pagina_gerador_vcf' é um nome para referenciar esta URL no Django
]