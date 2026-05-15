# 1. Altera as mensagens a escrever no ficheiro e verifica no ficheiro o que aconteceu.
# 2. Altera o modo de abertura do ficheiro para open("ficheiro.txt", "a") e verifica no ficheiro o que aconteceu.
# 3. Altera o modo de abertura do ficheiro para open("ficheiro.txt", "r") e verifica o resultado.

if __name__ == '__main__':
    with open("file1.txt", "w") as file:
        file.write("Hello, World!\n")
        file.write("This is a new line.")