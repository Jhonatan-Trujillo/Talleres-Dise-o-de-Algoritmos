"""
Crear un juego de ordenamiento de Barajas  de cartas , 
al iniciar se recibe un conjunto de cartas en total 13 cartas , 
la idea es que el algoritmo permita realizar el ordenamiento del maso de cartas con algunas
de las implementaciones vistas en clase.
Ejemplo

Recibo en total 52 cartas pero estas no estan ordenadas, 
primero debe establecer un ordenamiento por tipo de carta , trebol , corazones, 
aces o diamantes de cada una deben ser 13 cartas primero deben realizar un 
ordenamiento por color  y luego organizarlos por la numeracion de acuerdo a sus numeros al 
finalizer mostrar la baraja organizada

"""

def separar_cartas(baraja):
    baraja_separada = [carta[:-1] + "-" + carta[-1] for carta in baraja]
    for i in range(len(baraja_separada)):
        numero, palo = baraja_separada[i].split("-")
        if palo:
            baraja_separada[i] = [int(numero), palo]
    return baraja_separada

def separar_palos(baraja_separada):
    treboles = []
    corazones = []
    picas = []
    diamantes = []

    for numero, palo in baraja_separada:
        if palo == "T":
            treboles.append([numero, palo])
        elif palo == "C":
            corazones.append([numero, palo])
        elif palo == "P":
            picas.append([numero, palo])
        elif palo == "D":
            diamantes.append([numero, palo])
    
    return treboles, corazones, picas, diamantes

def selection_sort(lista):
    n = len(lista)

    # Recorremos toda la lista
    for i in range(n):
        # Suponemos que el primer elemento no ordenado es el mínimo
        indice_minimo = i

        # Buscamos el elemento más pequeño en el resto de la lista
        for j in range(i + 1, n):
            if lista[j] < lista[indice_minimo]:
                indice_minimo = j

        # Intercambiamos el mínimo encontrado con el elemento de la posición i
        lista[i], lista[indice_minimo] = lista[indice_minimo], lista[i]

    return lista


# ejemplo de baraja de treboles:
"""
treboles = [[7, "T"], [4, "T"], [12, "T"], 
[8, "T"], [1, "T"], [13, "T"], 
[10, "T"], [6, "T"], [3, "T"]]
"""
# Para los nombres de las carta
def formatear_carta(carta):
    numero, palo = carta
    # Nombre del número
    if numero == 1:
        numero_formateado = "As"
    elif numero == 11:
        numero_formateado = "J"
    elif numero == 12:
        numero_formateado = "Q"
    elif numero == 13:
        numero_formateado = "K"
    else:
        numero_formateado = str(numero)
    
    # Nombre del palo
    if palo == "T":
        palo = "Treboles"
    elif palo == "C":
        palo = "Corazones"
    elif palo == "P":
        palo = "Picas"
    elif palo == "D":
        palo = "Diamantes"
    
    return f"{numero_formateado} de {palo}"

# Para mostrar las cartas ordenadas por palo
def mostrar_palo(nombre, bajara_separada):
    print(f"\n{nombre}: ({len(bajara_separada)} cartas):")
    for carta in bajara_separada:
        print(f"{formatear_carta(carta)}")

# Baraja de cartas
baraja = [
    "7C", "1P", "13D", "4T", "11C", "9P", "2D", "12T",
    "6C", "3P", "10D", "8T", "5C", "12P", "1D", "13T",
    "2C", "9D", "11P", "4C", "7T", "10P", "3D", "6T",
    "13C", "5P", "8D", "1T", "12C", "2P", "11D", "9T",
    "4D", "7P", "10C", "6D", "3T", "13P", "5D", "8C",
    "11T", "2T", "12D", "9C", "4P", "1C", "7D", "10T",
    "3C", "6P", "8P", "5T"
]

baraja_separada = separar_cartas(baraja)
print(f"Baraja separada: {baraja_separada}")
treboles, corazones, picas, diamantes = separar_palos(baraja_separada)
T = selection_sort(treboles)
C = selection_sort(corazones)
P = selection_sort(picas)
D = selection_sort(diamantes)
print(f"\nTreboles: {T}\nCorazones: {C}\nPicas: {P}\nDiamantes: {D}\n")

mostrar_palo("Treboles", T)
mostrar_palo("Corazones", C)
mostrar_palo("Picas", P)
mostrar_palo("Diamantes", D)

poker_complete = T + C + P  + D

print("\n BARAJA COMPLETA ")
for carta in poker_complete:
    print(f"{formatear_carta(carta)}")
print(f"\nTotal de cartas : {len(poker_complete)}")