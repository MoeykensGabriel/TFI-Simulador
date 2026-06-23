# tema.py - colores, fuentes y medidas. unico lugar donde se tocan

from tkinter import ttk

# ----- Paleta de colores (moderna, slate + emerald) -----
COLORES = {
    # superficies
    "fondo":          "#EEF2F6",   # fondo general de la ventana
    "superficie":     "#FFFFFF",   # tarjetas / paneles
    "superficie_alt": "#F8FAFC",   # tarjetas secundarias
    "borde":          "#E2E8F0",   # bordes sutiles

    # paneles
    "panel_param":    "#FFFFFF",   # columna izquierda
    "panel_centro":   "#F8FAFC",   # columna central
    "panel_result":   "#FFFFFF",   # columna derecha
    "etiqueta_bar":   "#0F172A",   # barritas de titulo de cada columna

    # header / marca
    "header":         "#0F172A",   # barra superior (slate-900)
    "header_acento":  "#10B981",   # linea de acento bajo el header

    # accion principal
    "boton":            "#059669", # emerald-600
    "boton_hover":      "#047857", # emerald-700
    "boton_stop":       "#DC2626", # rojo (detener)
    "boton_stop_hover": "#B91C1C",
    "acento":           "#059669",

    # canales de salida
    "venta":          "#3B82F6",   # azul  - Canal de Reventa
    "reciclaje":      "#10B981",   # verde - Canal de Reciclaje
    "desecho":        "#64748B",   # slate - Canal de Desecho

    # estados (semaforo para deposito y alternativas)
    "ok":             "#10B981",
    "alerta":         "#F59E0B",
    "peligro":        "#EF4444",

    # tarjetas y textos
    "tarjeta":        "#FFFFFF",
    "texto":          "#0F172A",   # texto principal oscuro
    "texto_claro":    "#FFFFFF",   # texto sobre fondos oscuros
    "subtexto":       "#64748B",
}

# ----- Tipografias -----
FUENTES = {
    "titulo_app":     ("Segoe UI Semibold", 18, "bold"),
    "subtitulo_app":  ("Segoe UI", 10),
    "titulo_panel":   ("Segoe UI Semibold", 10, "bold"),
    "etiqueta":       ("Segoe UI", 10),
    "etiqueta_mini":  ("Segoe UI", 8),
    "valor_grande":   ("Segoe UI", 26, "bold"),
    "valor_medio":    ("Segoe UI", 14, "bold"),
    "valor_chico":    ("Segoe UI", 11, "bold"),
    "texto_normal":   ("Segoe UI", 9),
    "boton":          ("Segoe UI Semibold", 11, "bold"),
}

# ----- Medidas -----
MEDIDAS = {
    "ancho_ventana":  1180,
    "alto_ventana":   700,
    "ancho_param":    250,
    "ancho_result":   270,
    "padding":        14,
    "radio":          10,
}


def aplicar_estilo_ttk(root):
    """Estiliza los widgets ttk (combobox, scrollbar, progressbar) para que
    combinen con la paleta moderna en vez del look gris por defecto."""
    style = ttk.Style(root)
    try:
        style.theme_use("clam")
    except Exception:
        pass

    # Combobox
    style.configure(
        "TCombobox",
        fieldbackground=COLORES["superficie_alt"],
        background=COLORES["superficie_alt"],
        foreground=COLORES["texto"],
        bordercolor=COLORES["borde"],
        arrowcolor=COLORES["acento"],
        relief="flat",
        padding=4,
    )
    style.map(
        "TCombobox",
        fieldbackground=[("readonly", COLORES["superficie_alt"])],
        bordercolor=[("focus", COLORES["acento"])],
    )

    # Scrollbar
    style.configure(
        "Vertical.TScrollbar",
        background=COLORES["borde"],
        troughcolor=COLORES["fondo"],
        bordercolor=COLORES["fondo"],
        arrowcolor=COLORES["subtexto"],
        relief="flat",
    )

    # Progressbar (avance de semanas)
    style.configure(
        "Sim.Horizontal.TProgressbar",
        background=COLORES["acento"],
        troughcolor=COLORES["borde"],
        bordercolor=COLORES["borde"],
        thickness=10,
    )
