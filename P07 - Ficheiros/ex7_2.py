# 1. Verifica o conteudo do ficheiro
# 2. Depois de criado o ficheiro altera o codigo para ler o ficheiro e imprimir o conteudo
# 3. Altera o codigo para alterar 'apple' por 'maça' e 'cherry' por 'cereja' e guardar no ficheiro
# 4. Altera 'love' por 'chocolate'

import json

if __name__ == '__main__':
    my_list = ["apple", "banana", "cherry", {"secret_ingredient": "love"}]

    # Writing to a file
    with open("output.json", "w", encoding="utf-8") as file:
        json.dump(my_list, file, indent=4)
