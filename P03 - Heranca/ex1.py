# 1. Adiciona o metodo correr na class Animal
# 2. Adiciona na main c.correr()
# 3. Adiciona o metodo correr na class Cao. Observa o resultado
# 4. Adiciona o metodo correr na class Gato e na main g.correr(). Observa o resultado
# 5. Adiciona a funcao generica fazer_animal_correr e adiciona na main


class Animal:
    def falar(self):
        print("Som genérico")


class Cao(Animal):
    def falar(self):
        print("Au au")


class Gato(Animal):
    def falar(self):
        print("Miau")



def fazer_animal_falar(animal):
    animal.falar()

# main
if __name__ == "__main__":

    c = Cao()
    g = Gato()

    c.falar()
    g.falar()

    fazer_animal_falar(c)
    fazer_animal_falar(g)
