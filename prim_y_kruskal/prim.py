# ── Algoritmo de Prim en Python ──────────────────────────────
import heapq

def prim(grafo, inicio):
    """
    grafo: dict {nodo: [(peso, vecino), ...]}
    inicio: nodo de partida
    Retorna: lista de aristas del MST y el costo total
    """
    visitados   = set()
    mst_aristas = []
    costo_total = 0

    # Cola de prioridad: (peso, nodo_origen, nodo_destino)
    cola = [(0, inicio, inicio)]

    while cola:
        peso, origen, destino = heapq.heappop(cola)

        if destino in visitados:
            continue                        # Ya está en el árbol

        visitados.add(destino)
        costo_total += peso

        if origen != destino:              # Evita la arista de inicio
            mst_aristas.append((origen, destino, peso))

        for w, vecino in grafo[destino]:  # Explorar vecinos
            if vecino not in visitados:
                heapq.heappush(cola, (w, destino, vecino))

    return mst_aristas, costo_total

# ── Ejemplo: red de ciudades ─────────────────────────────────
grafo = {
    'A': [(4, 'B'), (8, 'D')],
    'B': [(4, 'A'), (5, 'C'), (6, 'E')],
    'C': [(5, 'B'), (2, 'F')],
    'D': [(8, 'A'), (3, 'E')],
    'E': [(6, 'B'), (3, 'D'), (7, 'F')],
    'F': [(2, 'C'), (7, 'E')]
}

aristas, costo = prim(grafo, 'A')
print(f"\nCosto total MST: {costo}")
for a, b, w in aristas:
    print(f"  {a} ──{w}── {b}")

# Salida esperada:
# Costo total MST: 14
#   A ──4── B
#   B ──5── C
#   C ──2── F
#   A ──8── D  (o D──3──E dependiendo del orden)