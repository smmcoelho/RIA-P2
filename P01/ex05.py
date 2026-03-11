# Estruturas de decisao


# if
a = 0
if a == 3:
    print("Numero 3")
elif a == 4:
    print("Numero 4")
else:
    print("Outro numero qualquer")


# match
b = 6
match b:
    case 3:
        print("Numero 3")
    case 4:
        print("Numero 4")
    case 5 | 6 | 7 | 8:
        print("Numero entre 5 e 8")
    case _:
        print("Numero desconhecido")