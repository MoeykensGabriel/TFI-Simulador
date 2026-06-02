# ============================================================
#  ventana_recomendaciones.py  -  Dialogo de Alternativas
# ------------------------------------------------------------
#  AQUI VA: la ventana emergente que muestra el diagnostico de
#  las 4 alternativas (A/B/C/D) con su recomendacion.
#  Sigue el mismo diseño visual de la app (tema.py).
#
#  RESPONSABILIDAD: solo MOSTRAR. Recibe la lista ya evaluada
#  desde alternativas.py.
# ============================================================

import tkinter as tk
from src.gui.tema import COLORES, FUENTES


class VentanaRecomendaciones:
    def __init__(self, parent, alternativas: list):
        self.win = tk.Toplevel(parent)
        self.win.title("Recomendaciones | Alternativas A/B/C/D")
        self.win.configure(bg=COLORES["fondo"])
        self.win.geometry("560x640")
        self.win.transient(parent)
        self._construir(alternativas)

    def _construir(self, alternativas):
        # --- Header (mismo estilo que la app) ---
        header = tk.Frame(self.win, bg=COLORES["header"], height=56)
        header.pack(fill="x")
        header.pack_propagate(False)
        tk.Label(header, text="RECOMENDACIONES PARA EL CLIENTE",
                 bg=COLORES["header"], fg=COLORES["texto_claro"],
                 font=FUENTES["titulo_panel"]).pack(side="left", padx=18, pady=14)

        # --- Contenedor con scroll ---
        cont = tk.Frame(self.win, bg=COLORES["fondo"], padx=14, pady=10)
        cont.pack(fill="both", expand=True)

        for a in alternativas:
            self._tarjeta(cont, a)

    def _tarjeta(self, parent, a):
        """Una tarjeta por alternativa, con franja de color segun estado."""
        # Rojo si hay accion requerida (condicion activa), verde si esta OK
        color = COLORES["venta"] if a["activa"] else COLORES["reciclaje"]
        estado = "ACCION REQUERIDA" if a["activa"] else "SIN CAMBIOS"

        card = tk.Frame(parent, bg=COLORES["tarjeta"], bd=0)
        card.pack(fill="x", pady=6)

        # Franja de color a la izquierda
        franja = tk.Frame(card, bg=color, width=8)
        franja.pack(side="left", fill="y")

        cuerpo = tk.Frame(card, bg=COLORES["tarjeta"], padx=12, pady=10)
        cuerpo.pack(side="left", fill="both", expand=True)

        # Titulo + badge de estado
        fila = tk.Frame(cuerpo, bg=COLORES["tarjeta"])
        fila.pack(fill="x")
        tk.Label(fila, text=f"Alternativa {a['id']}: {a['titulo']}",
                 bg=COLORES["tarjeta"], fg=COLORES["texto"],
                 font=FUENTES["titulo_panel"], anchor="w").pack(side="left")
        tk.Label(fila, text=estado, bg=color, fg="white",
                 font=FUENTES["texto_normal"], padx=8, pady=2).pack(side="right")

        # Condicion
        tk.Label(cuerpo, text=f"Condicion: {a['condicion']}",
                 bg=COLORES["tarjeta"], fg=COLORES["subtexto"],
                 font=FUENTES["texto_normal"], anchor="w",
                 wraplength=470, justify="left").pack(fill="x", pady=(6, 0))

        # Datos medidos
        tk.Label(cuerpo, text=a["datos"],
                 bg=COLORES["tarjeta"], fg=COLORES["texto"],
                 font=FUENTES["etiqueta"], anchor="w",
                 wraplength=470, justify="left").pack(fill="x", pady=(2, 0))

        # Recomendacion
        tk.Label(cuerpo, text=f"-> {a['recomendacion']}",
                 bg=COLORES["tarjeta"], fg=color,
                 font=FUENTES["etiqueta"], anchor="w",
                 wraplength=470, justify="left").pack(fill="x", pady=(6, 0))
