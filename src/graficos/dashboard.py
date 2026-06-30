# dashboard.py - graficas de matplotlib embebidas en tkinter, tematizadas

from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.ticker import FuncFormatter
from src.gui.tema import COLORES


def _nueva_figura():
    fig = Figure(figsize=(3.0, 1.8), dpi=100)
    fig.patch.set_facecolor(COLORES["superficie_alt"])
    ax = fig.add_subplot(111)
    ax.set_facecolor(COLORES["superficie_alt"])
    return fig, ax


def _estilizar(ax, titulo):
    ax.set_title(titulo, color=COLORES["texto"], fontsize=9, loc="left", pad=8)
    ax.tick_params(colors=COLORES["subtexto"], labelsize=7)
    for lado in ("top", "right"):
        ax.spines[lado].set_visible(False)
    for lado in ("left", "bottom"):
        ax.spines[lado].set_color(COLORES["borde"])
    ax.grid(axis="y", color=COLORES["borde"], linewidth=0.6, alpha=0.6)
    ax.set_axisbelow(True)


def _miles(valor):
    return f"{valor/1000:.0f}k" if abs(valor) >= 1000 else f"{valor:.0f}"


def _sin_datos(ax):
    ax.text(0.5, 0.5, "sin datos aun", ha="center", va="center",
            transform=ax.transAxes, color=COLORES["subtexto"], fontsize=8)
    ax.set_xticks([])
    ax.set_yticks([])


def crear_grafico_arribos(parent, semanas, arribos):
    """Barras: dispositivos que ingresaron en cada semana."""
    fig, ax = _nueva_figura()
    if semanas:
        ax.bar([f"S{s}" for s in semanas], arribos, color=COLORES["venta"], width=0.6)
        ax.yaxis.set_major_formatter(FuncFormatter(lambda v, _: _miles(v)))
    _estilizar(ax, "Arribos por semana")
    if not semanas:
        _sin_datos(ax)
    fig.tight_layout(pad=0.7)
    canvas = FigureCanvasTkAgg(fig, master=parent)
    canvas.draw()
    return canvas.get_tk_widget()


def crear_grafico_ganancias(parent, semanas, neta_acum):
    """Area + linea: ganancia neta acumulada semana a semana."""
    fig, ax = _nueva_figura()
    if semanas:
        etiquetas = [f"S{s}" for s in semanas]
        ax.plot(etiquetas, neta_acum, color=COLORES["reciclaje"], linewidth=2,
                marker="o", markersize=4)
        ax.fill_between(range(len(etiquetas)), neta_acum, color=COLORES["reciclaje"], alpha=0.18)
        ax.yaxis.set_major_formatter(FuncFormatter(lambda v, _: f"${_miles(v)}"))
    _estilizar(ax, "Ganancia neta acumulada")
    if not semanas:
        _sin_datos(ax)
    fig.tight_layout(pad=0.7)
    canvas = FigureCanvasTkAgg(fig, master=parent)
    canvas.draw()
    return canvas.get_tk_widget()
