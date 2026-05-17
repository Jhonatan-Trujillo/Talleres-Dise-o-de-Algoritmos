import json

def cargar_dataset(ruta: str) -> tuple:
    with open(ruta, "r", encoding="utf-8") as f:
        dataset = json.load(f)
    
    clientes = dataset["clientes"]
    matriz = dataset["matriz_distancias"]
    
    return clientes, matriz

# Greedy
def vecino_mas_cercano(matriz: list, inicio: int = 0) -> tuple:
    n = len(matriz)
    visitados = [False] * n
    ruta = [inicio]
    visitados[inicio] = True
    distancia_total = 0.0

    for _ in range(n - 1):
        actual = ruta[-1]
        mejor_vecino = -1
        mejor_distancia = float("inf")

        for j in range(n):
            if not visitados[j] and matriz[actual][j] < mejor_distancia:
                mejor_vecino = j
                mejor_distancia = matriz[actual][j]

        ruta.append(mejor_vecino)
        distancia_total += mejor_distancia
        visitados[mejor_vecino] = True

    # regresar al inicio
    distancia_total += matriz[ruta[-1]][inicio]
    ruta.append(inicio)

    return ruta, round(distancia_total, 2)

if __name__ == "__main__":
    clientes, matriz = cargar_dataset("data/clientes.json")
    ruta, distancia = vecino_mas_cercano(matriz)
    
    print("Ruta voraz (vecino más cercano):")
    for i, idx in enumerate(ruta):
        nombre = clientes[idx]["destino"] if idx < len(clientes) else "Depósito"
        print(f"  {i+1}. [{idx}] {nombre}")
    
    print(f"\nDistancia total: {distancia} metros ({round(distancia/1000, 2)} km)")
    print(f"Complejidad: O(n²) donde n={len(clientes)}")