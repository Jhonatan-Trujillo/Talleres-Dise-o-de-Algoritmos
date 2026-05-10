def separar_cartas(baraja):
    baraja_separada = [carta[:-1] + "-" + carta[-1] for carta in baraja]
    for i in range(len(baraja_separada)):
        numero, palo = baraja_separada[i].split("-")
        if palo:
            baraja_separada[i] = [int(numero), palo]
    return baraja_separada
"""
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
"""
def separar_por_palos(baraja_separada):
    palos = {}
    for carta in baraja_separada:
        numero, palo = carta
        if palo not in palos:
            palos[palo] = []
        palos[palo].append([numero, palo])
    return palos

def insertion_sort(lista):
    for i in range(1, len(lista)):
        clave = lista[i]
        j = i - 1
        while j >= 0 and clave[0] < lista[j][0]:
            lista[j + 1] = lista[j]
            j -= 1
        lista[j + 1] = clave
    return lista

def formatear_carta(carta):
    numero, palo = carta
    nombres = {1: "As", 11: "J", 12: "Q", 13: "K"}
    nombre_numero = nombres.get(numero, str(numero))
    nombre_palo = {"T": "Treboles", "C": "Corazones", "P": "Picas", "D": "Diamantes"}
    return f"{nombre_numero} de {nombre_palo[palo]}"

def mostrar_palo(nombre, bajara_separada):
    print(f"\n{nombre}: ({len(bajara_separada)} cartas):")
    for carta in bajara_separada:
        print(f"{formatear_carta(carta)}")

baraja = [
    "12P", "3D", "9C", "1T", "13C", "7P", "4D", "11T",
    "2C", "10P", "5T", "8D", "6C", "1P", "12D", "9T",
    "7C", "3P", "13D", "4T", "11C", "2D", "8P", "5C",
    "10T", "6D", "1C", "12T", "9P", "3C", "7D", "13P",
    "4C", "11D", "2T", "8C", "5P", "10D", "6T", "1D",
    "12C", "9D", "3T", "7T", "13T", "4P", "11P", "2P",
    "8T", "5D", "10C", "6P"
]

bajara_separada = separar_cartas(baraja)
palos = separar_por_palos(bajara_separada)

orden_palos = {"T": "Treboles", "C": "Corazones", "P": "Picas", "D": "Diamantes"}

for clave, nombre in orden_palos.items():
    cartas_ordenadas = insertion_sort(palos[clave])
    mostrar_palo(nombre, cartas_ordenadas)


poker_complete = []
for clave in orden_palos:
    poker_complete += palos[clave]

print("\n BARAJA COMPLETA ")
for carta in poker_complete:
    print(f"{formatear_carta(carta)}")
print(f"\nTotal de cartas : {len(poker_complete)}")
print(f"\nTreboles: {palos['T']}\nCorazones: {palos['C']}\nPicas: {palos['P']}\nDiamantes: {palos['D']}\n")
