from django.shortcuts import render
from .models import Dupla

def listar_duplas_view(request):
    todas_duplas = Dupla.objects.select_related('participante_1', 'participante_2')

    duplas_femininas = [d for d in todas_duplas if d.tipo == 'Feminina']
    duplas_masculinas = [d for d in todas_duplas if d.tipo == 'Masculina']
    duplas_mistas = [d for d in todas_duplas if d.tipo == 'Mista']

    context = {
        'duplas_femininas': duplas_femininas,
        'duplas_masculinas': duplas_masculinas,
        'duplas_mistas': duplas_mistas,
    }
    return render(request, 'campeonato_bt/lista_duplas.html', context)
