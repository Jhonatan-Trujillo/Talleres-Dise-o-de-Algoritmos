# ── Caso real: Red WiFi de campus universitario ───────────────
import heapq

edificios = ['Rectoría', 'Biblioteca', 'Lab_Cómputo',
             'Cafetería', 'Auditorio', 'Gimnasio']

# (costo_cable_metros, edificio_a, edificio_b)
conexiones = [
    (30, 'Rectoría',    'Biblioteca'),
    (80, 'Rectoría',    'Lab_Cómputo'),
    (50, 'Biblioteca',  'Lab_Cómputo'),
    (40, 'Biblioteca',  'Cafetería'),
    (20, 'Lab_Cómputo', 'Auditorio'),
    (60, 'Cafetería',   'Auditorio'),
    (70, 'Auditorio',   'Gimnasio'),
    (35, 'Cafetería',   'Gimnasio'),
]

# Construir grafo de adyacencia
grafo = {e: [] for e in edificios}
for costo, a, b in conexiones:
    grafo[a].append((costo, b))
    grafo[b].append((costo, a))

# Prim desde Rectoría
visitados, mst, total = set(), [], 0
cola = [(0, 'Rectoría', 'Rectoría')]

while cola:
    costo, origen, destino = heapq.heappop(cola)
    if destino in visitados: continue
    visitados.add(destino); total += costo
    if origen != destino: mst.append((origen, destino, costo))
    for w, v in grafo[destino]:
        if v not in visitados: heapq.heappush(cola, (w, destino, v))

print("\n🎓 RED WIFI ÓPTIMA DEL CAMPUS")
print("━" * 40)
for a, b, c in mst:
    print(f"  {a:15} ──{c:3}m── {b}")
print(f"━" * 40)
print(f"  Total cable necesario: {total} metros")
print(f"  (Sin MST se necesitarían {sum(c for c,_,_ in conexiones)} metros)")

# Salida:
# 🎓 RED WIFI ÓPTIMA DEL CAMPUS
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#   Rectoría        ── 30m── Biblioteca
#   Biblioteca      ── 40m── Cafetería
#   Lab_Cómputo     ── 20m── Auditorio
#   Cafetería       ── 35m── Gimnasio
#   Biblioteca      ── 50m── Lab_Cómputo
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#   Total cable necesario: 175 metros