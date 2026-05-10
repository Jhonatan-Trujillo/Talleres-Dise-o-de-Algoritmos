"""
📌 Problema 4 — LCS
Contexto: Control de versiones de código fuente

Dos versiones de un archivo de configuración:

v1: "DEPLOY-PROD-DB-01"
v2: "DEVELOP-DEBUG-01"

Halla la LCS entre ambas cadenas
Muestra la tabla dp completa
Reconstruye la subsecuencia mediante backtracking
¿Qué significa esta LCS en el contexto del versionado?
"""

# ─── Problema 4: LCS — Control de versiones ───────────────────────────────────

def lcs(v1: str, v2: str) -> dict:
    """
    Halla la Subsecuencia Común más Larga entre dos cadenas.

    Args:
        v1, v2 : las dos versiones del archivo de configuración

    Returns:
        dict con la tabla dp, la LCS reconstruida y su longitud
    """
    m, n = len(v1), len(v2)

    # 1. Inicializar tabla dp de ceros — (m+1) filas × (n+1) columnas
    #    dp[i][j] = longitud de la LCS entre v1[:i] y v2[:j]
    dp = [[0] * (n + 1) for _ in range(m + 1)]

    # 2. Llenar la tabla bottom-up
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if v1[i-1] == v2[j-1]:
                # Caracteres iguales → extender la LCS diagonal
                dp[i][j] = dp[i-1][j-1] + 1
            else:
                # Caracteres distintos → tomar el mejor vecino
                dp[i][j] = max(dp[i-1][j], dp[i][j-1])

    # 3. Backtracking: reconstruir la LCS recorriendo la tabla al revés
    lcs_chars = []
    i, j = m, n

    while i > 0 and j > 0:
        if v1[i-1] == v2[j-1]:
            # Los caracteres coinciden → forman parte de la LCS
            lcs_chars.append(v1[i-1])
            i -= 1
            j -= 1
        elif dp[i-1][j] > dp[i][j-1]:
            # Subir: la LCS viene de ignorar el carácter actual de v1
            i -= 1
        else:
            # Ir a la izquierda: la LCS viene de ignorar el carácter actual de v2
            j -= 1

    subsecuencia = "".join(reversed(lcs_chars))

    return {
        "tabla_dp"    : dp,
        "longitud"    : dp[m][n],
        "subsecuencia": subsecuencia,
    }


# ─── Datos del problema ────────────────────────────────────────────────────────
v1 = "DEPLOY-PROD-DB-01"
v2 = "DEVELOP-DEBUG-01"

resultado = lcs(v1, v2)

# ─── Resultados ───────────────────────────────────────────────────────────────
print(f"v1           : {v1}")
print(f"v2           : {v2}")
print(f"LCS          : {resultado['subsecuencia']}")
print(f"Longitud     : {resultado['longitud']}")
print(f"Similitud    : {resultado['longitud']*2/(len(v1)+len(v2))*100:.1f}%")

# Imprimir tabla dp (fragmento central para el informe)
print("\n=== TABLA DP (primeras 8 columnas) ===")
encabezado = "   " + "".join(f"{c:>4}" for c in ["-"] + list(v2[:7]))
print(encabezado)
for i, c in enumerate(["-"] + list(v1)):
    fila = f"{c:>2} " + "".join(f"{resultado['tabla_dp'][i][j]:>4}" for j in range(8))
    print(fila)