# 1. Na funcao __init__ commenta a linha com pass e descomenta o print
# 2. Define a variavel nome no contrutor (self.nome) e cria o metodo nome que retorna o nome
# 3. Cria a classe Gato com os mesmos metodos e adapta o metodo fala
# 4. Cria a classe Pessoa

class Cao:
    def __init__(self):
        # print("construtor")
        pass
    
    def fala(self):
        print("Au au")
    

# main 
if __name__ == "__main__":

    c = Cao() 
    c.fala()
