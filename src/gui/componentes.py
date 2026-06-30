# ============================================================
#  componentes.py  -  Widgets reutilizables
# ------------------------------------------------------------
#  AQUI VA: piezas visuales que se usan en VARIOS paneles, para
#  no repetir codigo (ej: la barrita de titulo de cada columna,
#  un campo de parametro con su etiqueta, una tarjeta de canal).
#  Pensalo como los "componentes" de React.
#  NO va logica de simulacion.
# ============================================================

import tkinter as tk
from tkinter import ttk
from src.gui.tema import COLORES, FUENTES


def titulo_panel(parent, texto):
    """Barra oscura con el titulo de una columna (ej: 'PARAMETROS')."""
    barra = tk.Frame(parent, bg=COLORES["etiqueta_bar"])
    barra.pack(fill="x", pady=(0, 12))
    # acento de color a la izquierda
    tk.Frame(barra, bg=COLORES["acento"], width=4).pack(side="left", fill="y")
    tk.Label(
        barra,
        text=texto,
        bg=COLORES["etiqueta_bar"],
        fg=COLORES["texto_claro"],
        font=FUENTES["titulo_panel"],
        pady=8,
        padx=10,
        anchor="w",
    ).pack(side="left", fill="x", expand=True)
    return barra


def campo_parametro(parent, etiqueta, opciones, valor_inicial):
    """
    Una etiqueta + un desplegable (combobox).
    Devuelve la variable para poder leer el valor elegido despues.
    Ejemplo de uso en panel_parametros.py.
    """
    tk.Label(
        parent,
        text=etiqueta,
        bg=parent["bg"],
        fg=COLORES["texto"],
        font=FUENTES["etiqueta"],
        anchor="w",
    ).pack(fill="x", pady=(8, 2))
    variable = tk.StringVar(value=str(valor_inicial))
    combo = ttk.Combobox(
        parent,
        textvariable=variable,
        values=[str(o) for o in opciones],
        state="readonly",
        font=FUENTES["texto_normal"],
    )
    combo.pack(fill="x")
    return variable

def campo_rango(parent, etiqueta, etiqueta_min, etiqueta_max, opciones_min, opciones_max, valor_min, valor_max):
    """
    Una etiqueta + dos dropdowns (Min y Max) en el mismo renglon.
    Devuelve dos variables: (var_min, var_max).
    """
    tk.Label(
        parent,
        text=etiqueta,
        bg=parent["bg"],
        fg=COLORES["texto"],
        font=FUENTES["etiqueta"],
        anchor="w",
    ).pack(fill="x", pady=(8, 2))

    fila = tk.Frame(parent, bg=parent["bg"])
    fila.pack(fill="x")

    # Min
    tk.Label(fila, text=etiqueta_min, bg=parent["bg"], fg=COLORES["subtexto"],
    font=FUENTES["texto_normal"]).pack(side="left")
    var_min = tk.StringVar(value=str(valor_min))
    ttk.Combobox(fila, textvariable=var_min, values=[str(o) for o in opciones_min],
    state="readonly", font=FUENTES["texto_normal"], width=4).pack(side="left", padx=(2, 10))

    # Max
    tk.Label(fila, text=etiqueta_max, bg=parent["bg"], fg=COLORES["subtexto"],
    font=FUENTES["texto_normal"]).pack(side="left")
    var_max = tk.StringVar(value=str(valor_max))
    ttk.Combobox(fila, textvariable=var_max, values=[str(o) for o in opciones_max],
    state="readonly", font=FUENTES["texto_normal"], width=4).pack(side="left", padx=(2, 0))

    return var_min, var_max

def campo_rango(parent, etiqueta, opciones_min, opciones_max, valor_min, valor_max,
                lbl_min="Min", lbl_max="Max"):
    """
    Una etiqueta + dos dropdowns en el mismo renglon (con etiquetas configurables).
    Devuelve dos variables: (var_min, var_max).
    """
    tk.Label(
        parent,
        text=etiqueta,
        bg=parent["bg"],
        fg=COLORES["texto"],
        font=FUENTES["etiqueta"],
        anchor="w",
    ).pack(fill="x", pady=(8, 2))

    fila = tk.Frame(parent, bg=parent["bg"])
    fila.pack(fill="x")

    tk.Label(fila, text=lbl_min, bg=parent["bg"], fg=COLORES["subtexto"],
             font=FUENTES["texto_normal"]).pack(side="left")
    var_min = tk.StringVar(value=str(valor_min))
    ttk.Combobox(fila, textvariable=var_min, values=[str(o) for o in opciones_min],
                 state="readonly", font=FUENTES["texto_normal"], width=4).pack(side="left", padx=(2, 10))

    tk.Label(fila, text=lbl_max, bg=parent["bg"], fg=COLORES["subtexto"],
             font=FUENTES["texto_normal"]).pack(side="left")
    var_max = tk.StringVar(value=str(valor_max))
    ttk.Combobox(fila, textvariable=var_max, values=[str(o) for o in opciones_max],
                 state="readonly", font=FUENTES["texto_normal"], width=4).pack(side="left", padx=(2, 0))

    return var_min, var_max


def tarjeta_canal(parent, nombre, color, valor="0"):
    """
    Tarjeta de color de un canal de salida (Venta/Reciclaje/Desecho)
    con su nombre y la cantidad de unidades.
    """
    card = tk.Frame(parent, bg=color, width=120, height=92)
    card.pack_propagate(False)

    # franja superior un poco mas oscura como acento
    tk.Frame(card, bg=color, height=6).pack(fill="x")
    lbl_valor = tk.Label(card, text=valor, bg=color, fg="white",
    font=FUENTES["valor_grande"])
    lbl_valor.pack(pady=(10, 0))
    tk.Label(card, text=nombre, bg=color, fg="white",
    font=FUENTES["texto_normal"]).pack()
    return card, lbl_valor


def metrica(parent, titulo, valor):
    """Tarjeta de resultado: etiqueta arriba, valor grande abajo, con borde."""
    card = tk.Frame(parent, bg=COLORES["superficie_alt"],
                    highlightbackground=COLORES["borde"], highlightthickness=1)
    card.pack(fill="x", pady=6)
    # acento de color a la izquierda
    tk.Frame(card, bg=COLORES["acento"], width=4).pack(side="left", fill="y")
    interior = tk.Frame(card, bg=COLORES["superficie_alt"], padx=12, pady=10)
    interior.pack(side="left", fill="x", expand=True)
    tk.Label(interior, text=titulo, bg=COLORES["superficie_alt"], fg=COLORES["subtexto"],
    font=FUENTES["etiqueta_mini"], anchor="w").pack(fill="x")
    lbl = tk.Label(interior, text=valor, bg=COLORES["superficie_alt"], fg=COLORES["texto"],
    font=FUENTES["valor_medio"], anchor="w")
    lbl.pack(fill="x")
    return lbl
