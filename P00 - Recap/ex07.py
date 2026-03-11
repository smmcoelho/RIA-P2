# Funcoes


def fazer() -> None:
    print("Fazer nada")

def algo(a: str) -> None:
    #a -> string
    print(f"imprimir {a}")

def algomais(a):
    #a -> qualquer
    print(f"imprimir {a}")

def soma(a: int, b: float) -> float:
    #a -> int
    #b -> float
    return a + b # return tipo float 



# main 
if __name__ == "__main__":
    fazer()
    algo("ola")
    algo(3) # funciona mas o IDE mostra um warning
    algomais(1)
    algomais(3.3)
    algomais('sim')
    print(f"{soma(1, 2.2)}")
