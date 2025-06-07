from django.shortcuts import render
from .models import Dupla
from itertools import combinations
import random
from itertools import combinations

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
    
    confrontos_mistos = gerar_confrontos_balanceados(duplas_mistas)

    context = {
        'duplas_femininas': duplas_femininas,
        'duplas_masculinas': duplas_masculinas,
        'duplas_mistas': duplas_mistas,
        'confrontos_mistos': confrontos_mistos,
    }

    return render(request, 'campeonato_bt/lista_duplas.html', context)

def equilibrar_confrontos(duplas):
    """
    Gera confrontos em ordem onde as duplas não jogam várias vezes seguidas.
    Baseado em um algoritmo round-robin com reordenação simples.
    """
    from collections import deque
    from itertools import combinations

    confrontos = list(combinations(duplas, 2))
    agenda = []
    ultima_dupla = None
    fila = deque(confrontos)

    while fila:
        for _ in range(len(fila)):
            confronto = fila.popleft()
            dupla1, dupla2 = confronto

            if ultima_dupla not in confronto:
                agenda.append(confronto)
                ultima_dupla = random.choice(confronto)  # Para embaralhar o foco
                break
            else:
                fila.append(confronto)
        else:
            # Nenhum confronto disponível sem repetição: força um (evita loop infinito)
            agenda.append(fila.popleft())
            ultima_dupla = None

    return agenda

def gerar_confrontos_balanceados(duplas):
    confrontos = list(combinations(duplas, 2))  # 15 confrontos únicos
    random.shuffle(confrontos)

    agenda = []
    tentativas = 0
    max_tentativas = 10000

    while tentativas < max_tentativas:
        agenda.clear()
        usados = set()

        for confronto in confrontos:
            dupla1, dupla2 = confronto

            if (
                not agenda or
                (dupla1 not in agenda[-1] and dupla2 not in agenda[-1])
            ):
                agenda.append(confronto)
            else:
                # Tenta reordenar novamente
                random.shuffle(confrontos)
                break

        if len(agenda) == 15:
            return agenda  # Sucesso

        tentativas += 1

    raise Exception("Não foi possível gerar agenda sem jogos consecutivos da mesma dupla.")