# 1. Faz com que o nome e o numero de pernas sejam passados ao construtor
# 2. Cria o metodo respode que imprime "Ao ao"
# 3. Cria o metodo buscar que imprime o que foi passado por parametro (Ex.O cao foi buscar a bola)
# 4. Move as funcoes cao e falar para um ficheiro chamado cao.py. Dica faz import
# 5. Adiciona uma variavel cor para atribuir a cor do cao e implementa o metodo cor
# 6. Adiciona a variavel raça e os respectivos metodos
# 7. Cria um metodo que altere o numero de pernas (minimo 1 e maximo 4)

class Cao:
    def __init__(self):
        self.nome = "Snoopy"
        self.pernas = 4

    def nome(self):
        return self.nome
    
    def pernas(self):
        return self.pernas
    
    def fala(self):
        return "Ao ao"


# main 
if __name__ == "__main__":

    c = Cao() 
    print(f"O {c.nome} tem {c.pernas} pernas" )
    print(f"O {c.nome} diz {c.fala()}" )
