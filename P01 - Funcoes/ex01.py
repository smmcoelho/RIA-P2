# 1. Faz com que o nome e o numero de pernas sejam parametros da funcao cao
# 2. Move as funcoes cao e falar para um ficheiro chamado cao.py. Dica faz import
# 3. Adiciona uma variavel cor para atribuir a cor do cao
# 4. Cria uma lista de caes e imprime o nome de todos os caes na lista
# 5. Cria um metodo para imprimir todas as variaveis da funcao cao

def cao():
    nome = "Snoopy"
    pernas = 4
    return [nome, pernas]

def falar():
    print("Ao ao")

# main 
if __name__ == "__main__":

    n, p = cao()

    print(f"o {n} tem {p} pernas")

    falar()