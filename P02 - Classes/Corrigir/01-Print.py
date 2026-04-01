# Corrigir codigo abaixo
# Tip: implementar __str__ , __repr__ ou __format__

class Carro:
    def __init__(self, marca, modelo):
        self.__marca = marca
        self.__modelo = modelo

if __name__ == '__main__':
    c1 = Carro("Fiat", "Uno")
    print(c1)   # Marca: Fiat - Modelo: Uno
