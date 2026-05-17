import json

def cargar_dataset(ruta: str) -> tuple:
    with open(ruta, "r", encoding="utf-8") as f:
        dataset = json.load(f)
    
    clientes = dataset["clientes"]
    matriz = dataset["matriz_distancias"]
    
    return clientes, matriz
def insertion_sort(clientes: list, distancias: list) -> list:
    # trabajamos con índices para no perder referencia a distancias
    indices = list(range(len(clientes)))
    
    for i in range(1, len(indices)):
        clave = indices[i]
        j = i - 1
        
        while j >= 0 and distancias[indices[j]] > distancias[clave]:
            indices[j + 1] = indices[j]    # desplaza hacia la derecha
            j -= 1
        
        indices[j + 1] = clave        # coloca la clave en su lugar
    
    return [clientes[i] for i in indices]

if __name__ == "__main__":
    clientes, matriz = cargar_dataset("data/clientes.json")
    ordenados = insertion_sort(clientes, distancias=[matriz[0][i] for i in range(len(clientes))])
    
    print("Clientes ordenados por distancia al depósito:")
    for i, c in enumerate(ordenados):
        idx = clientes.index(c)
        print(f"  {i+1}. {c['destino']} — {matriz[0][idx]} m")