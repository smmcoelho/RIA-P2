# Estruturas de decisao


# if
a = 7
if a == 3:
    print("Numero 3")
elif a == 4:
    print("Numero 4")
elif a in [5, 6]:
    print("Numero entre 5 e 6")
elif a in range(7, 9):
    print("Numero entre 7 e 8")
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