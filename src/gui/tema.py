# tema.py - colores, fuentes y medidas. soporta tema claro y oscuro

from tkinter import ttk

# ----- Paletas (clara y oscura) -----
PALETAS = {
    "claro": {
        "fondo":          "#EEF2F6",
        "superficie":     "#FFFFFF",
        "superficie_alt": "#F8FAFC",
        "borde":          "#E2E8F0",

        "panel_param":    "#FFFFFF",
        "panel_centro":   "#F8FAFC",
        "panel_result":   "#FFFFFF",
        "etiqueta_bar":   "#0F172A",

        "header":         "#0F172A",
        "header_acento":  "#10B981",

        "boton":            "#059669",
        "boton_hover":      "#047857",
        "boton_stop":       "#DC2626",
        "boton_stop_hover": "#B91C1C",
        "acento":           "#059669",

        "venta":          "#3B82F6",
        "reciclaje":      "#10B981",
        "desecho":        "#64748B",

        "ok":             "#10B981",
        "alerta":         "#F59E0B",
        "peligro":        "#EF4444",

        "tarjeta":        "#FFFFFF",
        "texto":          "#0F172A",
        "texto_claro":    "#FFFFFF",
        "subtexto":       "#64748B",
    },
    "oscuro": {
        "fondo":          "#0B1220",
        "superficie":     "#111A2B",
        "superficie_alt": "#0F1A2C",
        "borde":          "#1E293B",

        "panel_param":    "#111A2B",
        "panel_centro":   "#0D1626",
        "panel_result":   "#111A2B",
        "etiqueta_bar":   "#0B1220",

        "header":         "#0B1220",
        "header_acento":  "#22C55E",

        "boton":            "#16A34A",
        "boton_hover":      "#15803D",
        "boton_stop":       "#DC2626",
        "boton_stop_hover": "#B91C1C",
        "acento":           "#22C55E",

        "venta":          "#3B82F6",
        "reciclaje":      "#22C55E",
        "desecho":        "#64748B",

        "ok":             "#22C55E",
        "alerta":         "#F59E0B",
        "peligro":        "#EF4444",

        "tarjeta":        "#111A2B",
        "texto":          "#E2E8F0",
        "texto_claro":    "#FFFFFF",
        "subtexto":       "#94A3B8",
    },
}

# tema activo. el resto del codigo importa este dict y lee sus valores.
# aplicar_tema() lo muta en el lugar para que las referencias sigan validas.
COLORES = dict(PALETAS["claro"])
MODO_ACTUAL = "claro"


def aplicar_tema(modo: str) -> dict:
    """Cambia la paleta activa (claro/oscuro) mutando COLORES en el lugar."""
    global MODO_ACTUAL
    MODO_ACTUAL = modo if modo in PALETAS else "claro"
    COLORES.clear()
    COLORES.update(PALETAS[MODO_ACTUAL])
    return COLORES


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
    "alto_ventana":   720,
    "ancho_param":    250,
    "ancho_result":   320,
    "padding":        14,
    "radio":          10,
}


def aplicar_estilo_ttk(root):
    """Estiliza los widgets ttk segun el tema activo. Re-llamar al cambiar tema."""
    style = ttk.Style(root)
    try:
        style.theme_use("clam")
    except Exception:
        pass

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
        foreground=[("readonly", COLORES["texto"])],
        bordercolor=[("focus", COLORES["acento"])],
    )

    # lista desplegable del combobox
    root.option_add("*TCombobox*Listbox.background", COLORES["superficie_alt"])
    root.option_add("*TCombobox*Listbox.foreground", COLORES["texto"])
    root.option_add("*TCombobox*Listbox.selectBackground", COLORES["acento"])
    root.option_add("*TCombobox*Listbox.selectForeground", "#FFFFFF")

    style.configure(
        "Vertical.TScrollbar",
        background=COLORES["borde"],
        troughcolor=COLORES["fondo"],
        bordercolor=COLORES["fondo"],
        arrowcolor=COLORES["subtexto"],
        relief="flat",
    )

    style.configure(
        "Sim.Horizontal.TProgressbar",
        background=COLORES["acento"],
        troughcolor=COLORES["borde"],
        bordercolor=COLORES["borde"],
        thickness=10,
    )
