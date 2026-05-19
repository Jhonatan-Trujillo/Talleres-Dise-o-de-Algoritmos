import sys
import os
import time
import json

# Agregar ruta para imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from algoritmos.voraz import cargar_dataset, vecino_mas_cercano
from algoritmos.mochila_dp import cargar_datos, mochila_dp
from algoritmos.ordenamiento import insertion_sort
from algoritmos.backtracking import backtracking

def cargar_todo():
    with open("data/clientes.json", "r", encoding="utf-8") as f:
        dataset = json.load(f)
    with open("data/vehiculos.json", "r", encoding="utf-8") as f:
        vehiculos_data = json.load(f)
    
    return dataset["clientes"], dataset["matriz_distancias"], vehiculos_data["vehiculos"]

def mostrar_banner():
    print("=" * 50)
    print("       OPTIRUTA+ — Sistema de Ruteo")
    print("    Ibagué, Tolima — Colombia")
    print("=" * 50)

def exportar_mapa_data(clientes, matriz, ruta_voraz, vehiculos, distancia_voraz):
    import json

    # Puntos de clientes con coordenadas reales
    puntos = []
    for i, c in enumerate(clientes):
        puntos.append({
            "idx": i,
            "nombre": c["nombre"],
            "destino": c["destino"],
            "producto": c["producto"],
            "peso_kg": c["peso_kg"],
            "lat": c["latitud"],
            "lon": c["longitud"],
            "destino_lat": c["destino_latitud"],
            "destino_lon": c["destino_longitud"]
        })

    # Ruta voraz como secuencia de coordenadas
    ruta_voraz_coords = []
    for idx in ruta_voraz:
        if idx < len(clientes):
            ruta_voraz_coords.append({
                "idx": idx,
                "lat": clientes[idx]["latitud"],
                "lon": clientes[idx]["longitud"],
                "destino": clientes[idx]["destino"]
            })

    data = {
        "puntos": puntos,
        "ruta_voraz": ruta_voraz_coords,
        "distancia_voraz": distancia_voraz,
        "vehiculos": [v["tipo"] for v in vehiculos]
    }

    with open("data/mapa_data.json", "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    print("  ✓ mapa_data.json generado")

def main():
    mostrar_banner()
    N_CLIENTES = 8
    # ─── PASO 1: Cargar datos ─────────────────────
    print("\n[1/4] Cargando datos...")
    clientes, matriz, vehiculos = cargar_todo()
    print(f"  ✓ {len(clientes)} clientes cargados")
    print(f"  ✓ {len(vehiculos)} vehículos disponibles")
    print(f"  ✓ Matriz de distancias: {len(matriz)}x{len(matriz[0])}")

    # ─── PASO 2: Ordenar clientes ─────────────────
    print("\n[2/4] Ordenando clientes por distancia al depósito...")
    distancias = [matriz[0][i] for i in range(len(clientes))]
    ordenados = insertion_sort(clientes, distancias)
    print("  Clientes ordenados:")
    for i, c in enumerate(ordenados):
        idx = clientes.index(c)
        print(f"    {i+1}. {c['destino']} — {round(matriz[0][idx], 2)} m")
    
    # ─── PASO 3: Ruta voraz ────────────────────────
    print("\n[3/4] Calculando ruta inicial (Algoritmo Voraz)...")
    matriz_voraz = [fila[:N_CLIENTES] for fila in matriz[:N_CLIENTES]]
    ruta_voraz, distancia_voraz = vecino_mas_cercano(matriz_voraz)
    print(f"  Ruta: {ruta_voraz}")
    print(f"  Distancia total: {distancia_voraz} m ({round(distancia_voraz/1000, 2)} km)")
    print(f"  Complejidad: O(n²) donde n={N_CLIENTES}")

    # ─── PASO 3B: Mochila DP por vehículo ─────────
    print("\n  Asignación de paquetes por vehículo (Knapsack DP):")
    paquetes = [{"nombre": c["producto"], "peso": c["peso_kg"]} for c in clientes[:N_CLIENTES]]
    for vehiculo in vehiculos:
        capacidad = vehiculo["peso_max_kg"]
        peso_total, seleccionados = mochila_dp(capacidad, paquetes)
        print(f"  → {vehiculo['tipo']} ({capacidad}kg): {peso_total}kg cargados — {len(seleccionados)} paquetes")
    
    # ─── PASO 4: Backtracking ──────────────────────
    print("\n[4/4] Optimizando con Backtracking...")
    clientes_bt = clientes[:N_CLIENTES]
    matriz_bt = [fila[:N_CLIENTES] for fila in matriz[:N_CLIENTES]]
    pesos = [c["peso_kg"] for c in clientes_bt]

    _, distancia_voraz_bt = vecino_mas_cercano(matriz_bt)

    print(f"  Instancia: {N_CLIENTES} clientes")
    print(f"  Límite superior voraz: {distancia_voraz_bt} m")

    for vehiculo in vehiculos:
        capacidad = vehiculo["peso_max_kg"]
        archivo = f"data/pasos_{vehiculo['tipo']}.json"

        inicio = time.time()
        ruta, distancia = backtracking(matriz_bt, capacidad, pesos, distancia_voraz_bt, archivo)
        fin = time.time()

        print(f"\n  Vehículo: {vehiculo['tipo']} ({capacidad}kg)")
        if ruta:
            mejora = round(distancia_voraz_bt - distancia, 2)
            print(f"  Ruta óptima: {ruta}")
            print(f"  Distancia: {distancia} m — Mejora: {mejora} m")
        else:
            print(f"  Sin ruta factible — Voraz: {distancia_voraz_bt} m")
        print(f"  Tiempo: {round(fin - inicio, 4)}s")

    # ─── EXPORTAR DATOS PARA MAPA ──────────────────
    print("\nExportando datos para mapa interactivo...")
    exportar_mapa_data(clientes[:N_CLIENTES], matriz, ruta_voraz, vehiculos, distancia_voraz)

# ─── RESUMEN FINAL ─────────────────────────────
    print("\n" + "=" * 50)
    print("  RESUMEN COMPARATIVO")
    print("=" * 50)
    print(f"  Clientes:      {N_CLIENTES}")
    print(f"  Voraz:         {distancia_voraz} m — O(n²)")
    print(f"  Backtracking:  {distancia} m — O(n!) podado")
    print(f"  Mejora:        {round(distancia_voraz - distancia, 2)} m")
    print("=" * 50)
    print("\n✓ Archivos de pasos generados en data/")
    print("✓ Abre visualizacion/mapa.html para ver el mapa interactivo")
    print("✓ Abre visualizacion/index.html para ver el árbol de backtracking")

if __name__ == "__main__":
    main()