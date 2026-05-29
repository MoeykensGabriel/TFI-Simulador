# ============================================================
#  tema.py  -  Identidad visual del simulador
# ------------------------------------------------------------
#  AQUI VA: todos los colores, fuentes y medidas de la app.
#  NO va logica ni widgets. Es el unico lugar donde se tocan
#  los colores: si cambias un valor aca, cambia en toda la app.
# ============================================================

# ----- Paleta de colores (tomada del mockup) -----
COLORES = {
    # Fondos generales
    "header":         "#4CA77D",   # barra superior verde
    "panel_param":    "#5BB98C",   # fondo columna izquierda (parametros)
    "panel_centro":   "#D6E4F0",   # fondo columna central (flujo)
    "panel_result":   "#FFFFFF",   # fondo columna derecha (resultados)
    "fondo":          "#C8DCC4",   # fondo general de la ventana

    # Tarjetas y contenedores
    "tarjeta":        "#FFFFFF",
    "etiqueta_bar":   "#EAF2EA",   # barritas de titulo "PARAMETROS", etc.

    # Canales de salida
    "venta":          "#C0392B",   # rojo  - Canal de Reventa
    "reciclaje":      "#27AE60",   # verde - Canal de Reciclaje
    "desecho":        "#7F8C8D",   # gris  - Canal de Desecho

    # Accion principal
    "boton":          "#2E7D32",
    "boton_hover":    "#1B5E20",

    # Textos
    "texto":          "#1C2B2A",   # texto principal oscuro
    "texto_claro":    "#FFFFFF",   # texto sobre fondos oscuros
    "subtexto":       "#5A6B68",
}

# ----- Tipografias -----
FUENTES = {
    "titulo_app":   ("Segoe UI", 22, "bold"),
    "titulo_panel": ("Segoe UI", 10, "bold"),
    "etiqueta":     ("Segoe UI", 10),
    "valor_grande": ("Segoe UI", 22, "bold"),
    "valor_medio":  ("Segoe UI", 14, "bold"),
    "texto_normal": ("Segoe UI", 9),
    "boton":        ("Segoe UI", 11, "bold"),
}

# ----- Medidas -----
MEDIDAS = {
    "ancho_ventana":  1100,
    "alto_ventana":   560,
    "ancho_param":    230,   # ancho columna izquierda
    "ancho_result":   240,   # ancho columna derecha
    "padding":        12,
}
