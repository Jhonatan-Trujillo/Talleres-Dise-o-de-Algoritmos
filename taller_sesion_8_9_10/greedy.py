"""
🏧 Problema 1 — Sistema de cajero automático
Objetivo: dispensar $87.500 COP con billetes de 
[50000, 20000, 10000, 5000, 1000] usando el mínimo número de billetes.

¿Cómo piensa el algoritmo greedy aquí?
En cada paso toma el billete más grande posible que no supere el monto restante, 
lo usa tantas veces como pueda, y avanza al siguiente.
"""

# ─── Problema 1: Cajero ATM — Algoritmo Greedy ───────────────────────────────

def cajero_greedy(monto: int, billetes: list[int]) -> dict:
    """
    Dispensa un monto usando el mínimo número de billetes.
    
    Args:
        monto   : valor a dispensar en COP
        billetes: lista de denominaciones disponibles (se ordenan de mayor a menor)
    
    Returns:
        dict con la traza, billetes usados y resto sin cubrir
    """
    # 1. Ordenar de mayor a menor para garantizar la elección greedy correcta
    billetes = sorted(billetes, reverse=True)
    
    resto     = monto        # monto que falta por cubrir
    resultado = {}           # {billete: cantidad usada}
    traza     = []           # registro paso a paso para el informe

    # 2. Recorrer cada denominación
    for billete in billetes:
        if resto <= 0:
            break            # ya cubrimos el monto completo

        # 3. Elección greedy: ¿cuántas veces cabe este billete en el resto?
        cantidad = resto // billete      # división entera → sin decimales

        if cantidad > 0:
            resultado[billete] = cantidad
            descuento          = cantidad * billete
            traza.append({
                "billete"  : billete,
                "cantidad" : cantidad,
                "descuento": descuento,
                "resto"    : resto - descuento
            })
            resto -= descuento           # actualizar el resto

    return {
        "monto_original" : monto,
        "billetes_usados": resultado,
        "total_billetes" : sum(resultado.values()),
        "dispensado"     : monto - resto,
        "sin_cubrir"     : resto,
        "traza"          : traza
    }


# ─── Caso base: $87.500 ───────────────────────────────────────────────────────
denominaciones = [50000, 20000, 10000, 5000, 1000]
resultado = cajero_greedy(87500, denominaciones)

print("=== TRAZA: $87.500 COP ===")
for paso in resultado["traza"]:
    print(f"  {paso['cantidad']}x ${paso['billete']:,} = ${paso['descuento']:,}  →  resto: ${paso['resto']:,}")

print(f"\nTotal billetes: {resultado['total_billetes']}")
print(f"Dispensado    : ${resultado['dispensado']:,}")
print(f"Sin cubrir    : ${resultado['sin_cubrir']:,}")


# ─── Análisis: ¿qué pasa con billete de $7.000? ──────────────────────────────
denominaciones_7k = [50000, 20000, 10000, 7000, 5000, 1000]
r7 = cajero_greedy(87500, denominaciones_7k)

print("\n=== CON BILLETE DE $7.000 ===")
for paso in r7["traza"]:
    print(f"  {paso['cantidad']}x ${paso['billete']:,} = ${paso['descuento']:,}  →  resto: ${paso['resto']:,}")

print(f"\nTotal billetes: {r7['total_billetes']}")
print("¿Es óptimo? No, El greedy aún puede no serlo con denominaciones no canónicas.")