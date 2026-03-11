# 1. Altera a classe Coracao para receber 

class Coracao:
    def __init__(self):
        self.bpm = 120

    def bater(self):
        return "Tum-tum"


class Cao:
    def __init__(self, nome):
        self.nome = nome
        self.coracao = Coracao()  # composição

    def falar(self):
        return "Au au"

# main 
if __name__ == "__main__":
    # Uso
    c = Cao("Snoopy")
    print(c.coracao.bater())
