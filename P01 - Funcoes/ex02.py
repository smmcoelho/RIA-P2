# 1. Faz com que o nome e o numero de pernas sejam parametros da funcao pessoa
# 2. Adiciona uma variavel sobrenome 
# 3. Remove o metodo falar e adiciona falar ao dicionario
# 4. Cria uma lista de pessoas e imprime o sobrenome de todas os pessoas na lista
# 5. Faz com que uma pessoa so possa ser introduzida uma vez (conjunto nome + sobrenome nao pode ser repetido)

def pessoa():
    pessoa = {"nome": "John", "pernas": 2}
    return pessoa

def falar():
    print("Ola")

# main 
if __name__ == "__main__":

    p = pessoa()

    print(f"O {p["nome"]} tem {p["pernas"]} pernas")
    falar()