from django.urls import path
from . import views

urlpatterns = [
    path('duplas/', views.listar_duplas_view, name='listar_duplas'),
]
