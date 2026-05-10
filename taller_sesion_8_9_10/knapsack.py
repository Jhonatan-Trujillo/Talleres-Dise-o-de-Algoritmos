"""
📌 Problema 3 — Knapsack 0/1
Contexto: Proyecto de inversión en startups
Tienes $10M para invertir. Proyectos disponibles:

🏥 HealthTech
ROI: $7M
Costo: $3M
🤖 AI Startup
ROI: $9M
Costo: $5M
🌱 GreenTech
ROI: $4M
Costo: $2M
🚀 Fintech
ROI: $6M
Costo: $4M

Construye y llena la tabla dp completa
Identifica la cartera de inversión óptima
Implementa el backtracking para hallar los proyectos elegidos
"""

# ─── Problema 3: Knapsack 0/1 — Inversión en startups ─────────────────────────

def knapsack(proyectos: list[dict], capacidad: int) -> dict:
    """
    Resuelve el problema de la mochila 0/1 con programación dinámica.
    
    Args:
        proyectos : lista de dicts con 'nombre', 'roi', 'costo'
        capacidad : presupuesto máximo disponible (en M$)
    
    Returns:
        dict con la tabla dp, ROI óptimo y lista de proyectos elegidos
    """
    n  = len(proyectos)
    W  = capacidad

    # 1. Inicializar tabla dp de ceros — (n+1) filas × (W+1) columnas
    #    dp[i][w] = máximo ROI usando los primeros i proyectos con presupuesto w
    dp = [[0] * (W + 1) for _ in range(n + 1)]

    # 2. Llenar la tabla fila por fila (bottom-up)
    for i in range(1, n + 1):
        roi   = proyectos[i-1]["roi"]
        costo = proyectos[i-1]["costo"]

        for w in range(W + 1):
            if costo > w:
                # El proyecto no cabe → heredar valor anterior
                dp[i][w] = dp[i-1][w]
            else:
                # Elegir el máximo entre:
                #   - no incluir: dp[i-1][w]
                #   - incluir   : roi + lo mejor con el presupuesto restante
                dp[i][w] = max(
                    dp[i-1][w],
                    roi + dp[i-1][w - costo]
                )

    # 3. Backtracking: recorrer la tabla al revés para saber qué proyectos se eligieron
    elegidos = []
    w = W
    for i in range(n, 0, -1):
        # Si el valor cambió respecto a la fila anterior, este proyecto fue incluido
        if dp[i][w] != dp[i-1][w]:
            elegidos.append(proyectos[i-1]["nombre"])
            w -= proyectos[i-1]["costo"]   # reducir el presupuesto restante

    return {
        "tabla_dp"      : dp,
        "roi_optimo"    : dp[n][W],
        "cartera"       : list(reversed(elegidos)),
        "costo_total"   : W - w,
    }


# ─── Datos del problema ────────────────────────────────────────────────────────
proyectos = [
    {"nombre": "HealthTech", "roi": 7, "costo": 3},
    {"nombre": "AI Startup",  "roi": 9, "costo": 5},
    {"nombre": "GreenTech",   "roi": 4, "costo": 2},
    {"nombre": "Fintech",     "roi": 6, "costo": 4},
]

resultado = knapsack(proyectos, capacidad=10)

# ─── Imprimir tabla dp ────────────────────────────────────────────────────────
print("=== TABLA DP ===")
encabezado = "Item".ljust(12) + "".join(f"w={w:>3}" for w in range(11))
print(encabezado)
print("-" * len(encabezado))

for i, p in enumerate(proyectos):
    fila = f"{p['nombre'][:11]:<12}" + "".join(f"{'$'+str(v)+'M':>5}" for v in resultado["tabla_dp"][i+1])
    print(fila)

print(f"\nROI óptimo   : ${resultado['roi_optimo']}M")
print(f"Costo total  : ${resultado['costo_total']}M")
print(f"Cartera      : {' + '.join(resultado['cartera'])}")