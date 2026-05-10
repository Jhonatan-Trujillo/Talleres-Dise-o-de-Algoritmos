# ── Algoritmo de Kruskal con Union-Find ──────────────────────

class UnionFind:
    """Estructura para detectar ciclos eficientemente"""
    def __init__(self, nodos):
        self.padre = {n: n for n in nodos}   # cada nodo es su propio padre
        self.rango  = {n: 0 for n in nodos}

    def encontrar(self, x):
        if self.padre[x] != x:
            self.padre[x] = self.encontrar(self.padre[x])  # compresión
        return self.padre[x]

    def unir(self, x, y):
        rx, ry = self.encontrar(x), self.encontrar(y)
        if rx == ry:
            return False                    # Mismo componente → ciclo!
        if self.rango[rx] < self.rango[ry]:
            rx, ry = ry, rx
        self.padre[ry] = rx
        if self.rango[rx] == self.rango[ry]:
            self.rango[rx] += 1
        return True

def kruskal(nodos, aristas):
    """
    nodos:   lista de nodos
    aristas: lista de (peso, u, v)
    Retorna: MST y costo total
    """
    aristas_ord = sorted(aristas)              # ordenar por peso
    uf          = UnionFind(nodos)
    mst         = []
    costo_total = 0

    for peso, u, v in aristas_ord:
        if uf.unir(u, v):                      # No forma ciclo
            mst.append((u, v, peso))
            costo_total += peso
            if len(mst) == len(nodos) - 1:
                break                          # MST completo
    return mst, costo_total

# ── Ejemplo ──────────────────────────────────────────────────
nodos   = ['A', 'B', 'C', 'D', 'E', 'F']

aristas = [
    (4, 'A', 'B'), (8, 'A', 'D'), 
    (5, 'B', 'C'), (6, 'B', 'E'), 
    (2, 'C', 'F'), (3, 'D', 'E'), 
    (7, 'E', 'F')
]

mst, costo = kruskal(nodos, aristas)
print(f"\nCosto total MST: {costo}")
for u, v, w in mst:
    print(f"  {u} ──{w}── {v}")