# campeonato_bt/models.py

from django.db import models

class Participante(models.Model):
    NOME_GENEROS = [
        ('M', 'Masculino'),
        ('F', 'Feminino'),
    ]

    nome = models.CharField(max_length=100)
    genero = models.CharField(max_length=1, choices=NOME_GENEROS)

    def __str__(self):
        return self.nome


class Dupla(models.Model):
    participante_1 = models.ForeignKey(Participante, related_name='duplas_como_1', on_delete=models.CASCADE)
    participante_2 = models.ForeignKey(Participante, related_name='duplas_como_2', on_delete=models.CASCADE)

    criado_em = models.DateTimeField(auto_now_add=True)

    @property
    def tipo(self):
        g1 = self.participante_1.genero
        g2 = self.participante_2.genero
        if g1 == 'F' and g2 == 'F':
            return 'Feminina'
        elif g1 == 'M' and g2 == 'M':
            return 'Masculina'
        else:
            return 'Mista'

    def __str__(self):
        return f"{self.participante_1} & {self.participante_2}"
