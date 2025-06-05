# campeonato_bt/admin.py

from django.contrib import admin
from .models import Participante, Dupla

@admin.register(Participante)
class ParticipanteAdmin(admin.ModelAdmin):
    list_display = ('nome', 'genero', 'email', 'telefone')
    search_fields = ('nome', 'email')
    list_filter = ('genero',)

@admin.register(Dupla)
class DuplaAdmin(admin.ModelAdmin):
    list_display = ('participante_1', 'participante_2', 'tipo')
    search_fields = ('participante_1__nome', 'participante_2__nome')

    def tipo(self, obj):
        return obj.tipo
