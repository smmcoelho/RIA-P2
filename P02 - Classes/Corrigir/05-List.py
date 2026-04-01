# Corrigir codigo abaixo
# Tip: implementar __lt__
# Nao esquecer a  __str__ , __repr__ ou __format__

class Flor:
    def __init__(self, nome, cor):
        self.__nome = nome
        self.__cor = cor

if __name__ == '__main__':
    flores = [ Flor("Dalia", "Vermelha"),
               Flor("Margarida", "Azul"),
               Flor("Margarida", "Amarela"),
               Flor("Dalia", "Laranja")]

    flores.sort()
    for flor in flores:
        print(flor)

    # Resultado:
    # Nome: Dalia - Cor: Laranja
    # Nome: Dalia - Cor: Vermelha
    # Nome: Margarida - Cor: Amarela
    # Nome: Margarida - Cor: Azul
