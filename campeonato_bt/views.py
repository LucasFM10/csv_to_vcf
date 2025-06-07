from django.shortcuts import render
from .models import Dupla
from itertools import combinations
import random

def gerar_jogos_rodadas(duplas):
    confrontos = list(combinations(duplas, 2))
    random.shuffle(confrontos)  # embaralha para variar os confrontos

    rodadas = []
    while confrontos:
        rodada = []
        duplas_usadas = set()
        for a, b in confrontos[:]:
            if a not in duplas_usadas and b not in duplas_usadas:
                rodada.append((a, b))
                duplas_usadas.update([a, b])
                confrontos.remove((a, b))
        rodadas.append(rodada)
    return rodadas


def listar_duplas_view(request):
    todas_duplas = list(Dupla.objects.select_related('participante_1', 'participante_2'))

    duplas_femininas = [d for d in todas_duplas if d.tipo == 'Feminina']
    duplas_masculinas = [d for d in todas_duplas if d.tipo == 'Masculina']
    duplas_mistas = [d for d in todas_duplas if d.tipo == 'Mista']

    confrontos_mistos = list(combinations(duplas_mistas, 2))

    context = {
        'duplas_femininas': duplas_femininas,
        'duplas_masculinas': duplas_masculinas,
        'duplas_mistas': duplas_mistas,
        'confrontos_mistos': confrontos_mistos,
    }
    return render(request, 'campeonato_bt/lista_duplas.html', context)
