"""
📌 Problema 2 — Huffman
Contexto: Compresión de logs de un servidor

Un log repite las siguientes palabras: ERROR(45), INFO(120), WARN(30), DEBUG(80), TRACE(15).

Construye el árbol de Huffman paso a paso
Asigna códigos binarios a cada palabra
Calcula bits usados sin y con compresión
¿Qué porcentaje de espacio se ahorra?
"""

# ─── Problema 2: Código de Huffman — Compresión de logs ───────────────────────
import heapq

class NodoHuffman:
    """Nodo del árbol de Huffman."""
    def __init__(self, simbolo, frecuencia):
        self.simbolo    = simbolo     # nombre de la palabra (None si es nodo interno)
        self.frecuencia = frecuencia  # suma de frecuencias del subárbol
        self.izq        = None        # hijo izquierdo → bit 0
        self.der        = None        # hijo derecho   → bit 1

    # heapq compara nodos: el de menor frecuencia tiene prioridad
    def __lt__(self, otro):
        return self.frecuencia < otro.frecuencia


def construir_huffman(frecuencias: dict) -> NodoHuffman:
    """
    Construye el árbol de Huffman a partir de un diccionario {símbolo: frecuencia}.
    Retorna la raíz del árbol.
    """
    # 1. Crear un nodo hoja por cada símbolo e insertar en la cola de prioridad
    cola = [NodoHuffman(s, f) for s, f in frecuencias.items()]
    heapq.heapify(cola)          # convierte la lista en un min-heap → O(n)

    # 2. Repetir mientras haya más de un nodo en la cola
    while len(cola) > 1:
        # 3. Extraer los 2 nodos de menor frecuencia → decisión greedy
        izq = heapq.heappop(cola)
        der = heapq.heappop(cola)

        # 4. Crear nodo padre con la suma de frecuencias
        padre = NodoHuffman(simbolo=None, frecuencia=izq.frecuencia + der.frecuencia)
        padre.izq = izq
        padre.der = der

        # 5. Reinsertar el padre en la cola
        heapq.heappush(cola, padre)

    return cola[0]   # único nodo restante = raíz


def generar_codigos(nodo: NodoHuffman, prefijo: str = "", codigos: dict = None) -> dict:
    """
    Recorre el árbol en profundidad y asigna un código binario a cada hoja.
    Izquierda = '0', Derecha = '1'.
    """
    if codigos is None:
        codigos = {}

    if nodo.simbolo is not None:      # es hoja → guardar el código
        codigos[nodo.simbolo] = prefijo if prefijo else "0"
    else:                              # es nodo interno → descender
        generar_codigos(nodo.izq, prefijo + "0", codigos)
        generar_codigos(nodo.der, prefijo + "1", codigos)

    return codigos


def calcular_bits(frecuencias: dict, codigos: dict) -> dict:
    """Calcula bits con y sin Huffman, y el porcentaje de ahorro."""
    # Bits sin compresión: longitud en caracteres ASCII × 8 bits × frecuencia
    bits_sin = sum(len(s) * 8 * f for s, f in frecuencias.items())

    # Bits con Huffman: longitud del código × frecuencia
    bits_con = sum(len(codigos[s]) * f for s, f in frecuencias.items())

    ahorro_pct = (bits_sin - bits_con) / bits_sin * 100

    return {
        "bits_sin_huffman" : bits_sin,
        "bits_con_huffman" : bits_con,
        "bits_ahorrados"   : bits_sin - bits_con,
        "porcentaje_ahorro": round(ahorro_pct, 2)
    }


# ─── Datos del problema ────────────────────────────────────────────────────────
frecuencias = {
    "INFO" : 120,
    "DEBUG":  80,
    "ERROR":  45,
    "WARN" :  30,
    "TRACE":  15,
}

raiz    = construir_huffman(frecuencias)
codigos = generar_codigos(raiz)
stats   = calcular_bits(frecuencias, codigos)

# ─── Resultados ────────────────────────────────────────────────────────────────
print("=== CÓDIGOS DE HUFFMAN ===")
for simbolo, codigo in sorted(codigos.items(), key=lambda x: len(x[1])):
    bits_totales = len(codigo) * frecuencias[simbolo]
    print(f"  {simbolo:<6} f={frecuencias[simbolo]:>3}  código={codigo:<6}  "
          f"bits/ocurrencia={len(codigo)}  total={bits_totales}")

print(f"\nSin compresión : {stats['bits_sin_huffman']:,} bits")
print(f"Con Huffman    : {stats['bits_con_huffman']:,} bits")
print(f"Ahorro         : {stats['bits_ahorrados']:,} bits ({stats['porcentaje_ahorro']}%)")