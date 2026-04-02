"""
🏆 Torneo Deportivo (BST)
Eres el sistema de ranking de un torneo de e-sports.
Los jugadores tienen puntuaciones y necesitas un BST para gestionar las búsquedas eficientemente.

Tu tarea: Partiendo del BST implementado en la sección de código, agrega tres métodos:

a) minimo() — Retorna el jugador con menor puntuación.
b) maximo() — Retorna el jugador con mayor puntuación.
c) top_n(n) — Retorna los N jugadores con mayor puntuación.
"""

# Usa la clase BST del ejemplo anterior y agrégale:
class Nodo:
    def __init__(self, valor):
        self.valor = valor
        self.izquierda = None
        self.derecha = None


class BST:
    # ... (código anterior) ...
    def __init__(self):
        self.raiz = None

    def insertar(self, valor):
        self.raiz = self._insertar(self.raiz, valor)

    def _insertar(self, nodo, valor):
        if nodo is None:
            return Nodo(valor)
        if valor < nodo.valor:
            nodo.izquierda = self._insertar(nodo.izquierda, valor)
        elif valor > nodo.valor:
            nodo.derecha = self._insertar(nodo.derecha, valor)
        return nodo

    def buscar(self, valor):
        return self._buscar(self.raiz, valor)

    def _buscar(self, nodo, valor):
        if nodo is None or nodo.valor == valor:
            return nodo
        if valor < nodo.valor:
            return self._buscar(nodo.izquierda, valor)
        return self._buscar(nodo.derecha, valor)

    # InOrder: recorre izq → raíz → der (resultado ordenado)
    def inorder(self, nodo="__raiz__"):
        if nodo == "__raiz__":
            nodo = self.raiz
        if nodo:
            yield from self.inorder(nodo.izquierda)  # ← primero izquierda
            yield nodo.valor                          # ← luego el valor
            yield from self.inorder(nodo.derecha)    # ← luego derecha

    def reverse_inorder(self, nodo="__raiz__"):
        if nodo == "__raiz__":
            nodo = self.raiz
        if nodo:
            yield from self.reverse_inorder(nodo.derecha)  # ← primero derecha
            yield nodo.valor                              # ← luego el valor
            yield from self.reverse_inorder(nodo.izquierda)    # ← luego izquierda

    def minimo(self):
        # nodo actual → ¿tiene izquierda? → sí → muévete → ¿tiene izquierda? → no → ese es el mínimo
        nodo = self._minimo(self.raiz)
        return nodo.valor

    def _minimo(self, nodo):
        if nodo.izquierda:
            return self._minimo(nodo.izquierda)
        return nodo

    def maximo(self):
        # nodo actual → ¿tiene derecha? → sí → muévete → ¿tiene derecha? → no → ese es el máximo
        nodo = self._maximo(self.raiz)
        return nodo.valor
    
    def _maximo(self, nodo):
        if nodo.derecha:
            return self._maximo(nodo.derecha)
        return nodo

    def top_n(self, n):
        # Pista: InOrder da orden ascendente. ¿Cuál da descendente?
        return list(self.reverse_inorder())[:n]      


# Prueba:
torneo = BST()
puntos = [3200, 4100, 1800, 5000, 2700, 3900, 4600]
for p in puntos:
    torneo.insertar(p)
print("\n")
print("Mínimo:", torneo.minimo())  # → 1800
print("Máximo:", torneo.maximo())  # → 5000
print("Top 3:", torneo.top_n(3))  # → [5000, 4600, 4100]