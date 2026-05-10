import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

class UnionFind:
    def __init__(self, nodos):
        self.padre = {n: n for n in nodos}
        self.rango  = {n: 0 for n in nodos}

    def encontrar(self, x):
        if self.padre[x] != x:
            self.padre[x] = self.encontrar(self.padre[x])
        return self.padre[x]

    def unir(self, x, y):
        rx, ry = self.encontrar(x), self.encontrar(y)
        if rx == ry:
            return False
        if self.rango[rx] < self.rango[ry]:
            rx, ry = ry, rx
        self.padre[ry] = rx
        if self.rango[rx] == self.rango[ry]:
            self.rango[rx] += 1
        return True

def kruskal(nodos, aristas):
    aristas_ord = sorted(aristas)
    uf          = UnionFind(nodos)
    mst         = []
    costo_total = 0
    for peso, u, v in aristas_ord:
        if uf.unir(u, v):
            mst.append((u, v, peso))
            costo_total += peso
            if len(mst) == len(nodos) - 1:
                break
    return mst, costo_total

nodos = ['A', 'B', 'C', 'D', 'E', 'F', 'G']

aristas = [
    (7,  'A', 'B'), (5,  'A', 'C'),
    (4,  'B', 'C'), (6,  'B', 'D'),
    (9,  'B', 'E'), (3,  'C', 'F'),
    (8,  'C', 'G'), (2,  'D', 'E'),
    (11, 'E', 'F'), (10, 'F', 'G'),
]

pos = {
    'A': (3.0, 4.0),
    'B': (1.5, 3.0),
    'C': (4.5, 3.0),
    'D': (0.0, 2.0),
    'E': (2.0, 2.0),
    'F': (3.5, 2.0),
    'G': (5.5, 2.0),
}

mst, costo_total = kruskal(nodos, aristas)
print(f"\nCosto total MST: {costo_total}")
for u, v, w in mst:
    print(f"  {u} ──{w}── {v}")

# IMPLEMETACION DEL MATPLOTLIB
COLOR_FONDO     = '#0f1117'
COLOR_MST       = '#1D9E75'
COLOR_DESC      = '#3a3a4a'
COLOR_NODO      = '#378ADD'
COLOR_BORDE     = '#185FA5'
COLOR_TEXTO     = 'white'
COLOR_PESO_MST  = '#5DCAA5'
COLOR_PESO_DESC = '#555566'

fig, axes = plt.subplots(1, 2, figsize=(14, 6))
fig.patch.set_facecolor(COLOR_FONDO)

def dibujar(ax, titulo, subtitulo, mostrar_descartadas=True):
    ax.set_facecolor(COLOR_FONDO)
    ax.set_xlim(-0.5, 6.2)
    ax.set_ylim(1.2, 4.8)
    ax.axis('off')

    for peso, u, v in aristas:
        x1, y1 = pos[u]
        x2, y2 = pos[v]
        en_mst  = (u, v, peso) in mst

        if not en_mst and not mostrar_descartadas:
            continue

        color = COLOR_MST  if en_mst else COLOR_DESC
        lw    = 3.0        if en_mst else 1.2
        ls    = '-'        if en_mst else '--'
        alpha = 1.0        if en_mst else 0.55
        ax.plot([x1, x2], [y1, y2], color=color, linewidth=lw,
                linestyle=ls, alpha=alpha, zorder=1)

        mx, my  = (x1 + x2) / 2, (y1 + y2) / 2
        fc = COLOR_PESO_MST  if en_mst else COLOR_PESO_DESC
        fs = 10              if en_mst else 9
        fw = 'bold'          if en_mst else 'normal'
        ax.text(mx, my, str(peso), color=fc, fontsize=fs, fontweight=fw,
                ha='center', va='center', zorder=3,
                bbox=dict(boxstyle='round,pad=0.25', fc=COLOR_FONDO, ec='none'))

    for n, (x, y) in pos.items():
        circle = plt.Circle((x, y), 0.22, color=COLOR_NODO,
                             ec=COLOR_BORDE, linewidth=2, zorder=4)
        ax.add_patch(circle)
        ax.text(x, y, n, color=COLOR_TEXTO, fontsize=13, fontweight='bold',
                ha='center', va='center', zorder=5)

    ax.set_title(titulo, color=COLOR_TEXTO, fontsize=13, fontweight='bold', pad=10)
    ax.text(0.5, 0.01, subtitulo, transform=ax.transAxes,
            ha='center', color='#9F9F9F', fontsize=9)

dibujar(axes[0],
        titulo='Grafo completo',
        subtitulo='Verde = MST  |  Gris punteado = descartada',
        mostrar_descartadas=True)

dibujar(axes[1],
        titulo='MST óptimo — Kruskal',
        subtitulo=f'Costo total: {costo_total} M$  |  6 aristas para 7 nodos',
        mostrar_descartadas=False)

leyenda = [
    mpatches.Patch(color=COLOR_MST,  label='Tubería instalada (MST)'),
    mpatches.Patch(color=COLOR_DESC, label='Conexión descartada'),
    mpatches.Patch(color=COLOR_NODO, label='Barrio'),
]
fig.legend(handles=leyenda, loc='lower center', ncol=3, fontsize=9,
           facecolor='#1a1a2e', edgecolor='none', labelcolor='white',
           bbox_to_anchor=(0.5, -0.02))

plt.suptitle('Red de Acueducto — 7 Barrios', color='white',
             fontsize=15, fontweight='bold', y=1.01)
plt.tight_layout()
plt.savefig('mst_acueducto.png', dpi=150,
            bbox_inches='tight', facecolor=fig.get_facecolor())
print("Imagen guardada: mst_acueducto.png")