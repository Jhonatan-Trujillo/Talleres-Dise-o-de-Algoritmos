import requests
import time

# ─────────────────────────────────────────────
# 1. OBTENER DATOS DE LA API
# ─────────────────────────────────────────────
def obtener_paises():
    """
    Consume la API de restcountries y retorna
    la lista de países europeos.
    """
    url = "https://restcountries.com/v3.1/region/europe"
    try:
        respuesta = requests.get(url)
        respuesta.raise_for_status()  # Lanza una excepción para códigos de error HTTP
        paises = []
        for p in respuesta.json():
            paises.append({
                "nombre": p["name"]["common"].lower(),
                "googleMaps": p["maps"]["googleMaps"]
            })
        return paises
    except Exception as e:
        print(f"Error al conectar con la API: {e}")
        return []    
    
# ─────────────────────────────────────────────
# 2. ALGORITMOS DE ORDENAMIENTO
# ─────────────────────────────────────────────
def insertion_sort(lista):
    for i in range(1, len(lista)):
        clave = lista[i]
        j = i - 1
        while j >= 0 and clave["nombre"] < lista[j]["nombre"]:
            lista[j + 1] = lista[j]
            j -= 1
        lista[j + 1] = clave
    return lista

def selection_sort(lista):
    n = len(lista)
    for i in range(n):
        # Asume que el mínimo está en la posición actual
        indice_minimo = i

        # Busca si hay un elemento más pequeño en el resto de la lista
        for j in range(i + 1, n):
            if lista[j]["nombre"] < lista[indice_minimo]["nombre"]:
                indice_minimo = j

        # Intercambia el mínimo encontrado con la posición actual
        lista[i], lista[indice_minimo] = lista[indice_minimo], lista[i]

    return lista

# ─────────────────────────────────────────────
# 3. BÚSQUEDA LINEAL
# ─────────────────────────────────────────────
def busqueda_lineal(paises, nombre_buscado):

    nombre_buscado = nombre_buscado.lower()  # Ignorar mayúsculas/minúsculas

    for i in range(len(paises)):
        # Comparamos el nombre común del país (en inglés) con el buscado
        nombre_pais = paises[i]["nombre"]
        if nombre_pais == nombre_buscado:
            return i  # ¡Encontrado! Retorna el índice

    return -1  # No se encontró

# ─────────────────────────────────────────────
# 4. BÚSQUEDA BINARIA
# ─────────────────────────────────────────────
def busqueda_binaria(paises_ordenados, nombre_buscado):

    nombre_buscado = nombre_buscado.lower()

    izquierda = 0
    derecha = len(paises_ordenados) - 1

    while izquierda <= derecha:
        medio = (izquierda + derecha) // 2  # Índice del elemento del centro
        nombre_medio = paises_ordenados[medio]["nombre"]

        if nombre_medio == nombre_buscado:
            return medio  # ¡Encontrado!
        elif nombre_medio < nombre_buscado:
            izquierda = medio + 1  # Buscar en la mitad derecha
        else:
            derecha = medio - 1   # Buscar en la mitad izquierda

    return -1  # No se encontró

# ─────────────────────────────────────────────
# 5. MOSTRAR INFORMACIÓN DEL PAÍS
# ─────────────────────────────────────────────
def mostrar_resultado(pais):
    print("\n  Se encontró el país:")
    print(f"   Nombre     : {pais['nombre'].title()}")
    print(f"   Google Maps: {pais['googleMaps']}")

# ─────────────────────────────────────────────
# 6. MEDIR TIEMPO DE ORDENAMIENTO
# ─────────────────────────────────────────────
def medir_tiempo_ordenamiento(paises, algoritmo):
    """
    Ejecuta el algoritmo de ordenamiento y mide cuánto tarda.
    Retorna la lista ordenada y el tiempo en milisegundos.
    """
    # Hacemos una copia para que ambos algoritmos partan de la misma lista desordenada
    lista_copia = paises.copy()
    
    inicio = time.time()             # ← marca el inicio
    lista_ordenada = algoritmo(lista_copia)
    fin = time.time()                # ← marca el fin
    
    tiempo_ms = (fin - inicio) * 1000  # convertimos a milisegundos
    return lista_ordenada, tiempo_ms

# ─────────────────────────────────────────────
# 7. MEDIR TIEMPO DE BÚSQUEDA
# ─────────────────────────────────────────────
def medir_tiempo_busqueda(paises, nombre_buscado, algoritmo_busqueda):
    """
    Ejecuta el algoritmo de búsqueda y mide cuánto tarda.
    Retorna el índice encontrado y el tiempo en milisegundos.
    """
    inicio = time.time()
    resultado = algoritmo_busqueda(paises, nombre_buscado)
    fin = time.time()

    tiempo_ms = (fin - inicio) * 1000
    return resultado, tiempo_ms

# ─────────────────────────────────────────────
# 8. MENU
# ─────────────────────────────────────────────
opcion = 0
while opcion != "3":
    print("\n\n\n=== MENÚ DE BÚSQUEDA DE PAÍSES EUROPEOS ===")
    print("\n1. Realizar Búsqueda Lineal")
    print("2. Realizar Búsqueda Binaria")
    print("3. Salir")
    try:
        opcion = input("\nSelecciona una opción: ")
    except ValueError:
        print("\nOpción no válida. Por favor, selecciona 1, 2 o 3.")
    else:
        if opcion == "1":
            paises = obtener_paises()
            try:
                nombre_buscado = input("\nIngresa el nombre del país a buscar en ingles: ")
            except ValueError:
                print("\n Entrada no válida. Por favor, ingresa un nombre de país.")
            else:
                resultado_busqueda, tiempo_busqueda = medir_tiempo_busqueda(paises, nombre_buscado, busqueda_lineal)
                print(f"\n⏱ Tiempo de búsqueda lineal: {tiempo_busqueda:.4f} ms")
                if resultado_busqueda != -1:
                    mostrar_resultado(paises[resultado_busqueda])
                else:
                    print("\n País no encontrado.")

        elif opcion == "2":
            paises = obtener_paises()
            eleccion = 0
            while eleccion != "3":
                print("\n\n=== MÉTODO DE ORDENAMIENTO PARA BÚSQUEDA BINARIA ===")
                print("\n1. Ordenar con Insertion Sort")
                print("2. Ordenar con Selection Sort")
                print("3. Volver al menú principal")
                try:
                    eleccion = input("\nSelecciona un algoritmo de ordenamiento: ")
                except ValueError:
                    print("\nOpción no válida. Por favor, selecciona 1, 2 o 3.")
                    continue                                      
                
                if eleccion == "1":
                    paises_ordenados, tiempo_ordenamiento = medir_tiempo_ordenamiento(paises, insertion_sort)
                    print(f"\nPaíses ordenados con Insertion Sort.")
                    print(f"⏱ Tiempo de ordenamiento: {tiempo_ordenamiento:.4f} ms")

                elif eleccion == "2":
                    paises_ordenados, tiempo_ordenamiento = medir_tiempo_ordenamiento(paises, selection_sort)
                    print(f"\nPaíses ordenados con Selection Sort.")
                    print(f"⏱ Tiempo de ordenamiento: {tiempo_ordenamiento:.4f} ms")
                elif eleccion == "3":
                    break                                         
                else:
                    print("\nOpción no válida. Por favor, selecciona 1, 2 o 3.")
                    continue      
                try:
                    nombre_buscado = input("\nIngresa el nombre del país a buscar en ingles: ")
                except ValueError:
                    print("\n Entrada no válida. Por favor, ingresa un nombre de país.")
                else:
                    resultado_busqueda, tiempo_busqueda = medir_tiempo_busqueda(paises_ordenados, nombre_buscado, busqueda_binaria)
                    print(f"\n⏱ Tiempo de ordenamiento : {tiempo_ordenamiento:.4f} ms")
                    print(f"⏱ Tiempo de búsqueda     : {tiempo_busqueda:.4f} ms")
                    print(f"⏱ Tiempo total           : {tiempo_ordenamiento + tiempo_busqueda:.4f} ms")
                    if resultado_busqueda != -1:
                        mostrar_resultado(paises_ordenados[resultado_busqueda])
                    else:
                        print("\n País no encontrado.")

        elif opcion == "3":
            print("\n¡Hasta luego!")
        else:
            print("\nOpción no válida. Por favor, selecciona 1, 2 o 3.")