# Corrigir codigo abaixo
# Tip: implementar __eq__

class Flor:
    def __init__(self, nome, cor):
        self.__nome = nome
        self.__cor = cor

    def __repr__(self):
        return f"Nome: {self.__nome} - Cor: {self.__cor}"

    def __hash__(self):
        return hash((self.__nome, self.__cor))

if __name__ == '__main__':
    flores = {Flor("Dalia", "Vermelha"),
              Flor("Margarida", "Azul"),
              Flor("Margarida", "Amarela"),
              Flor("Dalia", "Vermelha")}

    for flor in flores:
        print(flor)

    # Resultado:
    # Nome: Margarida - Cor: Amarela
    # Nome: Dalia - Cor: Vermelha
    # Nome: Margarida - Cor: Azul
