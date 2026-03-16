# EJERCICIO RECURSIVIDAD

def retroceder(historial, pasos):
    #Caso base 1: si no hay pasos, se devuelve el historial actual
    if pasos == 0:
        return historial
    #Caso base 2: si el último elemento es "Error 404", se detiene el retroceso
    if historial[-1] == "Error 404":
        print("Error 404 encontrado, deteniendo retroceso.")
        return historial
    #Eliminar el último elemento del historial
    historial.pop() # Elimina historial[-1]
    return retroceder(historial, pasos - 1)

#Ejercicio
historial = ["google.com", "facebook.com", "twitter.com", 
             "Error 404", "linkedin.com", "github.com", "youtube.com"]

print("\nHistorial actual: ", historial)
historial = retroceder(historial, 4)
print("Historial Final: ", historial)