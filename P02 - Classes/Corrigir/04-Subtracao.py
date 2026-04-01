# Corrigir codigo abaixo
# Tip: implementar __sub__
# Nao esquecer a  __str__ , __repr__ ou __format__


class Produto:
    def __init__(self, nome, preco):
        self.__nome = nome
        self.__preco = preco

if __name__ == '__main__':
    p1 = Produto("Camisa", 50)
    p2 = Produto("Camisola", 120)

    print(p1)
    print(p2)

    total = p1 - p2
    print("Total:", total)  # Total: 170
