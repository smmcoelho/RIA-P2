# 1. Faz com que o nome e o numero de pernas sejam passados ao construtor
# 2. Instancia outro cao na main
# 3. Adiciona o metodo print que deve imprimir as 2 mensagens da main (e remove os prints chamando este novo metodo)
# 4. Cria o metodo respode que imprime "Ao ao"
# 5. Cria o metodo buscar que imprime o que foi passado por parametro (Ex.O cao foi buscar a bola)
# 6. Move a class Cao para um ficheiro chamado cao.py. Dica faz import
# 7. Adiciona uma variavel cor para atribuir a cor do cao e implementa o metodo cor
# 8. Adiciona a variavel raça e os respectivos metodos
# 9. Cria um metodo que altere o numero de pernas (minimo 1 e maximo 4). Dica usa excepcoes ou um booleano para retornar o sucesso da accao)

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
