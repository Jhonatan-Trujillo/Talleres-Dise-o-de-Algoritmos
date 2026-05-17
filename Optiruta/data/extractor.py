import osmnx as ox
import networkx as nx
import json
import random
import requests
import time

# ─── CONFIGURACIÓN ────────────────────────────────────────────
CIUDAD = "Ibagué, Tolima, Colombia"

DESTINOS_FIJOS = [
    "Centro Comercial Multicentro Ibagué",
    "Centro Comercial La Estación Ibagué",
    "Parque Centenario Ibagué",
    "Plaza de Bolívar Ibagué",
    "Terminal de Transportes Ibagué",
    "Aeropuerto Perales Ibagué",
    "Hospital Federico Lleras Acosta Ibagué",
    "Universidad del Tolima Ibagué",
    "Universidad de Ibagué",
    "Estadio Manuel Murillo Toro Ibagué",
    "Parque de la Música Ibagué",
    "Hospital San Francisco Ibagué",
    "Barrio El Salado Ibagué",
    "Chapetón Ibagué",
    "Picaleña Ibagué"
]

PRODUCTOS = [
    "Nevera", "Caja de frutas", "Televisor", "Colchón",
    "Caja de libros", "Electrodoméstico", "Ropa empacada",
    "Caja de medicamentos", "Computador", "Mueble desmontado",
    "Caja de herramientas", "Juguetes", "Documentos", 
    "Caja de alimentos secos", "Botellón de agua", "Equipo deportivo", "Caja de productos electrónicos",
    "Spray de limpieza", "Labial rojo", "Pala", "Bicicleta"
]

# ─── 1. CARGAR GRAFO (osmnx) ──────────────────────────────────
def cargar_grafo():
    print("Descargando grafo de Ibagué...")
    G = ox.graph_from_place(CIUDAD, network_type="drive")
    print(f"Grafo cargado: {len(G.nodes())} nodos, {len(G.edges())} aristas")
    return G

# ─── 2. BUSCAR DESTINOS (Nominatim) ───────────────────────────
def buscar_destinos():
    print("\nBuscando coordenadas de destinos con Nominatim...")
    destinos = []

    for nombre in DESTINOS_FIJOS:
        url = "https://nominatim.openstreetmap.org/search"
        params = {
            "q": nombre,
            "format": "json",
            "countrycodes": "co",
            "limit": 1
        }
        headers = {"User-Agent": "OptiroutaPlus/1.0"}
        respuesta = requests.get(url, params=params, headers=headers)
        resultados = respuesta.json()

        if resultados:
            r = resultados[0]
            destinos.append({
                "nombre": nombre,
                "latitud": float(r["lat"]),
                "longitud": float(r["lon"])
            })
            print(f"  ✓ {nombre}")
        else:
            print(f"  ✗ No encontrado: {nombre}")

        time.sleep(1)

    print(f"Destinos encontrados: {len(destinos)}")
    return destinos

# ─── 3. PUENTE: coordenadas → nodos del grafo (osmnx) ─────────
def destinos_a_nodos(G, destinos):
    print("\nMapeando destinos al grafo de calles...")
    destinos_con_nodo = []

    for d in destinos:
        nodo_id = ox.nearest_nodes(G, X=d["longitud"], Y=d["latitud"])
        data = G.nodes[nodo_id]
        destinos_con_nodo.append({
            "nombre": d["nombre"],
            "latitud_real": d["latitud"],
            "longitud_real": d["longitud"],
            "node_id": nodo_id,
            "latitud_nodo": data["y"],
            "longitud_nodo": data["x"]
        })
        print(f"  ✓ {d['nombre']} → nodo {nodo_id}")

    return destinos_con_nodo

# ─── 4. EXTRAER CLIENTES (combina todo) ───────────────────────
def extraer_clientes(G, destinos_con_nodo, n=15):
    print(f"\nGenerando {n} clientes...")
    nodos = list(G.nodes(data=True))
    seleccionados = random.sample(nodos, n)

    clientes = []
    for node_id, data in seleccionados:
        destino = random.choice(destinos_con_nodo)
        cliente = {
            "node_id": node_id,
            "nombre": f"Cliente_{node_id}",
            "latitud": data["y"],
            "longitud": data["x"],
            "peso_kg": round(random.uniform(1.0, 50.0), 2),
            "volumen": [
                round(random.uniform(10.0, 100.0), 1),
                round(random.uniform(10.0, 100.0), 1),
                round(random.uniform(10.0, 100.0), 1)
            ],
            "producto": random.choice(PRODUCTOS),
            "origen": "Centro de distribución Ibagué",
            "destino": destino["nombre"],
            "destino_latitud": destino["latitud_real"],
            "destino_longitud": destino["longitud_real"],
            "destino_node_id": destino["node_id"]
        }
        clientes.append(cliente)
        print(f"  ✓ {cliente['nombre']} → {cliente['destino']}")

    return clientes

# ─── 5. MATRIZ DE DISTANCIAS (networkx) ───────────────────────
def calcular_distancias(G, clientes):
    print("\nCalculando matriz de distancias reales...")
    n = len(clientes)
    matriz = [[0.0] * n for _ in range(n)]

    for i in range(n):
        for j in range(n):
            if i != j:
                try:
                    distancia = nx.shortest_path_length(
                        G,
                        clientes[i]["node_id"],
                        clientes[j]["node_id"],
                        weight="length"
                    )
                    matriz[i][j] = round(distancia, 2)
                except nx.NetworkXNoPath:
                    matriz[i][j] = float("inf")

    print(f"Matriz {n}x{n} calculada")
    return matriz

# ─── MAIN ─────────────────────────────────────────────────────
if __name__ == "__main__":
    G = cargar_grafo()
    destinos = buscar_destinos()
    destinos_con_nodo = destinos_a_nodos(G, destinos)
    clientes = extraer_clientes(G, destinos_con_nodo, n=15)
    matriz = calcular_distancias(G, clientes)

    dataset = {
        "clientes": clientes,
        "destinos_disponibles": destinos_con_nodo,
        "matriz_distancias": matriz
    }

    with open("data/clientes.json", "w", encoding="utf-8") as f:
        json.dump(dataset, f, ensure_ascii=False, indent=2)

    print("\n✓ Dataset completo guardado en data/clientes.json")