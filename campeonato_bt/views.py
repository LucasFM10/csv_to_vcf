from django.shortcuts import render
from .models import Dupla
from itertools import combinations

def listar_duplas_view(request):
    todas_duplas = list(Dupla.objects.select_related('participante_1', 'participante_2'))

    duplas_femininas = [d for d in todas_duplas if d.tipo == 'Feminina']
    duplas_masculinas = [d for d in todas_duplas if d.tipo == 'Masculina']
    duplas_mistas = [d for d in todas_duplas if d.tipo == 'Mista']

    # Ordena por ID para manter determinismo
    duplas_mistas.sort(key=lambda d: d.id)

    # Divide em duas chaves
    chave_a = duplas_mistas[:3]
    chave_b = duplas_mistas[3:6]

    # Fase de grupos (3 confrontos por chave)
    jogos_fase_grupos = list(combinations(chave_a, 2)) + list(combinations(chave_b, 2))

    # Nome dos confrontos (str para o template)
    confrontos_fase_grupos = [(a, b) for a, b in jogos_fase_grupos]

    # Jogos eliminatórios (semifinais, disputa de 3º e final)
    # Para fins de exibição, usamos placeholders
    semifinal_1 = ("1º Chave A", "2º Chave B")
    semifinal_2 = ("1º Chave B", "2º Chave A")
    disputa_3 = ("Perdedor Semi 1", "Perdedor Semi 2")
    final = ("Vencedor Semi 1", "Vencedor Semi 2")

    confrontos_eliminatorios = [
        semifinal_1,
        semifinal_2,
        disputa_3,
        final,
    ]

    context = {
        'duplas_femininas': duplas_femininas,
        'duplas_masculinas': duplas_masculinas,
        'duplas_mistas': duplas_mistas,
        'chave_a': chave_a,
        'chave_b': chave_b,
        'confrontos_fase_grupos': confrontos_fase_grupos,
        'confrontos_eliminatorios': confrontos_eliminatorios,
    }

    return render(request, 'campeonato_bt/lista_duplas.html', context)
