"""
🗺️ Sistema de Metro (BFS)
Imagina que eres el desarrollador de la app del Metro de Bogotá. 
Tienes un grafo no dirigido donde cada estación es un nodo y cada vía entre estaciones es una arista.

Tu tarea: Implementa una función ruta_minima(grafo, origen, destino) 
usando BFS que retorne la lista de estaciones del recorrido más corto (menor número de paradas) 
entre dos estaciones. Si no existe camino, retorna None.
"""
from collections import deque

"""deque: estructura de datos tipo lista optimizada para operaciones de inserción y eliminación en 
ambos extremos (cola doble)"""

# TU SOLUCIÓN AQUÍ:
# ---- BFS: Búsqueda en Anchura (nivel por nivel) ----
"""def bfs(grafo, inicio):
    visitados = set()
    cola = deque([inicio])
    visitados.add(inicio)
    orden = []

    while cola:
        nodo = cola.popleft()
        orden.append(nodo)

        for vecino, _ in grafo.lista_adyacencia.get(nodo, []):
            if vecino not in visitados:
                visitados.add(vecino)
                cola.append(vecino)

    return orden
"""
def ruta_minima(grafo, origen, destino): # funcion que inicia la búsqueda del camino mínimo
    # Pista: usa BFS con seguimiento del camino
    visitados = set() # conjunto para marcar estaciones visitadas y evitar ciclos
    cola = deque([[origen]])  # ← cada elemento es un camino completo
    visitados.add(origen) #  ← marcamos el origen como visitado

    while cola: # mientras haya caminos por explorar
        camino = cola.popleft() # ← sacamos el camino (lista)
        nodo = camino[-1] # ← el nodo actual es el último de la lista

        if nodo == destino: # ← hemos llegado al destino
            return camino   # ← encontramos el camino

        for vecino in grafo.get(nodo, []):  # ← este camino llegó al destino ✓
            if vecino not in visitados: # ← si el vecino no ha sido visitado
                visitados.add(vecino) # ← marcamos el vecino como visitado
                cola.append(camino + [vecino])  # ← lista con el camino completo

    return None # no existe camino


# Prueba:
metro = {
    "Portal Norte":   ["Toberín"],
    "Toberín":        ["Portal Norte", "Calle 142"],
    "Calle 142":      ["Toberín", "Calle 127"],
    "Calle 127":      ["Calle 142", "Pepe Sierra", "Alcalá"],
    "Pepe Sierra":    ["Calle 127", "Niza"],
    "Alcalá":         ["Calle 127", "Calle 100"],
    "Niza":           ["Pepe Sierra", "Calle 100"],
    "Calle 100":      ["Alcalá", "Niza", "Virrey"],
    "Virrey":         ["Calle 100", "Centro"],
    "Centro":         ["Virrey", "Portal Sur"],
    "Portal Sur":     ["Centro"],
}

print("\n", ruta_minima(metro, "Portal Norte", "Centro"))
# Esperado: ['Portal Norte', 'Toberín', 'Calle 142',
#            'Calle 127', 'Alcalá', 'Calle 100', 'Virrey', 'Centro']
print("\n", ruta_minima(metro, "Portal Norte", "Portal Sur"))
# Esperado: ['Portal Norte', 'Toberín', 'Calle 142',
#            'Calle 127', 'Alcalá', 'Calle 100', 'Virrey', 'Centro', 'Portal Sur']