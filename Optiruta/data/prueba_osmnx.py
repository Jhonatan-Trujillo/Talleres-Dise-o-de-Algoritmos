import osmnx as ox

ciudad = "Ibagué, Tolima, Colombia"
G = ox.graph_from_place(ciudad, network_type="drive")
nodos = list(G.nodes())
inicio = nodos[0]
final = nodos[500]
print(inicio)
print(final)

import networkx as nx
ruta = nx.shortest_path(G, inicio, final, weight="length")
ox.plot_graph_route(G, ruta, route_linewidth=4, node_size=0)