#1. Na main, crie um cao e imprima seu nome.
#2. Crie um coracao e imprima seu bpm.
#3. Crie um dono e adicione um cao.
#4. Crie um veterinario e adicione um cao.
#5. Imprima o nome do veterinario do cao.

class Animal:
    def __init__(self, nome):
        self.nome = nome


class Coracao:
    def __init__(self, bpm=90):
        self.bpm = bpm


class Cao(Animal):  # HERANÇA
    def __init__(self, nome, raca):
        super().__init__(nome)
        self.raca = raca
        self.coracao = Coracao()  # COMPOSIÇÃO: criado dentro do cão
        self.veterinario = None   # ASSOCIAÇÃO: referência opcional

    def marcar_consulta(self, vet):
        self.veterinario = vet    # associação: usa um Veterinario


class Dono:  # AGREGAÇÃO com Cao
    def __init__(self, nome):
        self.nome = nome
        self.caes = []            # cães vêm de fora

    def adicionar_cao(self, cao):
        self.caes.append(cao)     # não controla o ciclo de vida do cão


class Veterinario:
    def __init__(self, nome):
        self.nome = nome


if __name__ == '__main__':
    #TODO
    
