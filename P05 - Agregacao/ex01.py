class Cao:
    def __init__(self, nome):
        self.nome = nome

    def falar(self):
        return "Au au"


class Dono:
    def __init__(self, nome):
        self.nome = nome
        self.animais = []  # lista de cães adotados

    def adotar(self, animal):
        self.animais.append(animal)  # agregação


# main 
if __name__ == "__main__":
    # Uso
    cao1 = Cao("Snoopy")   # existe sozinho
    dono = Dono("Carlos")

    dono.adotar(cao1)      # dono passa a ter o cão, mas não o cria

    if len(dono.animais) > 0:
        print(dono.animais[0].falar())
