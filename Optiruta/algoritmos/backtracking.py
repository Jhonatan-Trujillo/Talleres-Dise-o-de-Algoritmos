import json
import time
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from algoritmos.voraz import vecino_mas_cercano

def cargar_dataset(ruta_clientes: str, ruta_vehiculos: str) -> tuple:
    with open(ruta_clientes, "r", encoding="utf-8") as f:
        dataset = json.load(f)
    
    with open(ruta_vehiculos, "r", encoding="utf-8") as f:
        vehiculos_data = json.load(f)
    
    clientes = dataset["clientes"]
    matriz = dataset["matriz_distancias"]
    vehiculos = vehiculos_data["vehiculos"]
    
    return clientes, matriz, vehiculos

def backtracking(matriz: list, capacidad: float, pesos: list, mejor_voraz: float, archivo_pasos="data/pasos_backtracking.json") -> tuple:
    n = len(matriz)
    pasos = []  # registro de cada paso del backtracking
    mejor_ruta = []
    mejor_distancia = [mejor_voraz]

    def explorar(ruta, visitados, dist_actual, peso_actual):
        if len(ruta) == n:
            dist_total = dist_actual + matriz[ruta[-1]][0]
            if dist_total < mejor_distancia[0]:
                mejor_distancia[0] = dist_total
                mejor_ruta.clear()
                mejor_ruta.extend(ruta + [0])
                pasos.append({"tipo": "mejor_ruta", "ruta": list(ruta), "distancia": dist_total})
            return
        
        for j in range(1, n):
            if not visitados[j]:
                nueva_dist = dist_actual + matriz[ruta[-1]][j]
                nuevo_peso = peso_actual + pesos[j]
                
                if nueva_dist >= mejor_distancia[0]:
                    pasos.append({"tipo": "poda_distancia", "ruta": list(ruta), "rechazado": j})
                    continue
                
                if nuevo_peso > capacidad:
                    pasos.append({"tipo": "poda_peso", "ruta": list(ruta), "rechazado": j})
                    continue
                
                pasos.append({"tipo": "explorar", "ruta": list(ruta), "siguiente": j})
                visitados[j] = True
                ruta.append(j)
                explorar(ruta, visitados, nueva_dist, nuevo_peso)
                ruta.pop()
                visitados[j] = False
                pasos.append({"tipo": "backtrack", "ruta": list(ruta), "desde": j})

    visitados_inicio = [False] * n
    visitados_inicio[0] = True
    explorar([0], visitados_inicio, 0.0, 0.0)
    with open(archivo_pasos, "w", encoding="utf-8") as f:
        json.dump({"pasos": pasos, "n": n}, f)
    print(f"Pasos guardados: {len(pasos)}")

    return mejor_ruta, mejor_distancia[0]

if __name__ == "__main__":
    import sys
    sys.setrecursionlimit(100000) # limite de recursión para backtracking
    
    N_CLIENTES = 8 

    clientes, matriz, vehiculos = cargar_dataset("data/clientes.json", "data/vehiculos.json")
    
    clientes = clientes[:N_CLIENTES]
    matriz = [fila[:N_CLIENTES] for fila in matriz[:N_CLIENTES]]
    pesos = [c["peso_kg"] for c in clientes]
    
    for vehiculo in vehiculos:

        capacidad = vehiculo["peso_max_kg"]

        ruta_voraz, mejor_voraz = vecino_mas_cercano(matriz)

        print("\n==============================")
        print(f"Vehículo: {vehiculo['tipo']}")
        print(f"Capacidad: {capacidad}kg")
        print(f"Clientes en instancia: {N_CLIENTES}")
        print(f"Límite superior voraz: {mejor_voraz}m")
        print("Ejecutando backtracking...")
    
        archivo = f"data/pasos_{vehiculo['tipo']}.json"
        inicio = time.time()
        ruta, distancia = backtracking(matriz, capacidad, pesos, mejor_voraz, archivo)
        fin = time.time()
    
        if ruta:
            print(f"\nMejor ruta encontrada: {ruta}")
            print(f"Distancia óptima: {distancia}m")
            print(f"Mejora vs voraz: {round(mejor_voraz - distancia, 2)}m")
        else:
            print("\nNo se encontró ruta factible")
            print(f"Mejor distancia voraz: {mejor_voraz}m")
        
        print(f"Tiempo de ejecución: {round(fin - inicio, 4)}s")
        print(f"Complejidad: O(n!) podado")