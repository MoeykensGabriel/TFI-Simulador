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
    """Barrita gris clara con el titulo de una columna (ej: 'PARAMETROS')."""
    barra = tk.Label(
        parent,
        text=texto,
        bg=COLORES["etiqueta_bar"],
        fg=COLORES["texto"],
        font=FUENTES["titulo_panel"],
        pady=4,
    )
    barra.pack(fill="x", pady=(0, 10))
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

def campo_rango(parent, etiqueta, opciones_min, opciones_max, valor_min, valor_max):
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
    tk.Label(fila, text="Min", bg=parent["bg"], fg=COLORES["subtexto"],
             font=FUENTES["texto_normal"]).pack(side="left")
    var_min = tk.StringVar(value=str(valor_min))
    ttk.Combobox(fila, textvariable=var_min, values=[str(o) for o in opciones_min],
                 state="readonly", font=FUENTES["texto_normal"], width=4).pack(side="left", padx=(2, 10))

    # Max
    tk.Label(fila, text="Max", bg=parent["bg"], fg=COLORES["subtexto"],
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
    card = tk.Frame(parent, bg=color, width=110, height=70)
    card.pack_propagate(False)

    tk.Label(card, text=nombre, bg=color, fg="white",
    font=FUENTES["valor_medio"]).pack(pady=(6, 0))
    lbl_valor = tk.Label(card, text=valor, bg=color, fg="white",
    font=FUENTES["valor_grande"])
    lbl_valor.pack()
    return card, lbl_valor


def metrica(parent, titulo, valor):
    """Un resultado de texto: titulo arriba, valor grande abajo."""
    tk.Label(parent, text=titulo, bg=parent["bg"], fg=COLORES["subtexto"],
    font=FUENTES["texto_normal"]).pack(pady=(10, 0))
    lbl = tk.Label(parent, text=valor, bg=parent["bg"], fg=COLORES["texto"],
    font=FUENTES["valor_medio"])
    lbl.pack()
    return lbl
