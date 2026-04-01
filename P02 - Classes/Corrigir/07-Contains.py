# Corrigir codigo abaixo
# Tip: na class Florista implementar __contains__

class Flor:
    def __init__(self, nome, cor):
        self.__nome = nome
        self.__cor = cor

    def __repr__(self):
        return f"{self.nome} ({self.cor})"


class Florista:
    def __init__(self):
        self.flores = []

    def adicionar(self, flor):
        self.flores.append(flor)


if __name__ == "__main__":
    f1 = Flor("Rosa", "Vermelha")
    f2 = Flor("Tulipa", "Amarela")

    loja = Florista()
    loja.adicionar(f1)

    print(f1 in loja)   # True
    print(f2 in loja)   # False
