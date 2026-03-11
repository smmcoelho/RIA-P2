

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

    fazer_animal_falar(Cao())

    fazer_animal_falar(Gato())
