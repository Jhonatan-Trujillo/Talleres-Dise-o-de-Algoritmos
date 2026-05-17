import json

def cargar_datos(ruta_clientes: str, ruta_vehiculos: str) -> tuple:
    with open(ruta_clientes, "r", encoding="utf-8") as f:
        dataset = json.load(f)
    
    with open(ruta_vehiculos, "r", encoding="utf-8") as f:
        vehiculos_data = json.load(f)
    
    clientes = dataset["clientes"]
    vehiculos = vehiculos_data["vehiculos"]
    
    return clientes, vehiculos

def mochila_dp(capacidad: float, paquetes: list) -> tuple:
    n = len(paquetes)
    C = int(capacidad)
    pesos = [int(p["peso"]) for p in paquetes]

    # construir tabla dp
    dp = [[0] * (C + 1) for _ in range(n + 1)]

    for i in range(1, n + 1):
        for w in range(C + 1):
            if pesos[i-1] > w:
                dp[i][w] = dp[i-1][w]          # no cabe, no lo tomo
            else:
                dp[i][w] = max(
                    dp[i-1][w],                # no lo tomo
                    dp[i-1][w - pesos[i-1]] + pesos[i-1]    # lo tomo
                )

    # reconstruir cuáles paquetes se seleccionaron
    seleccionados = []
    w = C
    for i in range(n, 0, -1):
        if dp[i][w] != dp[i-1][w]:
            seleccionados.append(paquetes[i-1]["nombre"])
            w -= pesos[i-1]

    return dp[n][C], seleccionados

if __name__ == "__main__":
    clientes, vehiculos = cargar_datos("data/clientes.json", "data/vehiculos.json")
    
    for vehiculo in vehiculos:
        capacidad = vehiculo["peso_max_kg"]
        paquetes = [{"nombre": c["producto"], "peso": c["peso_kg"]} for c in clientes]
        
        peso_total, seleccionados = mochila_dp(capacidad, paquetes)
        
        print(f"\nVehículo: {vehiculo['tipo']} (capacidad {capacidad}kg)")
        print(f"Peso total cargado: {peso_total}kg de {capacidad}kg")
        print(f"Paquetes ({len(seleccionados)}): {seleccionados}")
        print(f"Complejidad: O(n×C) donde n={len(paquetes)}, C={int(capacidad)}")