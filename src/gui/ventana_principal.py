# ============================================================
#  VentanaPrincipal - Ventana raiz de la aplicacion
#  Muestra la pantalla de bienvenida y gestiona la navegacion
# ============================================================

import tkinter as tk
from tkinter import ttk, font


# Paleta de colores del simulador
COLORES = {
    "fondo":        "#1E1E2E",   # fondo oscuro principal
    "panel":        "#2A2A3E",   # fondo de paneles
    "acento":       "#7C3AED",   # violeta UTN / accion principal
    "acento_hover": "#6D28D9",
    "rojo":         "#EF4444",   # canal Reventa
    "verde":        "#22C55E",   # canal Reciclaje
    "gris":         "#6B7280",   # canal Desecho
    "texto":        "#F1F5F9",
    "subtexto":     "#94A3B8",
}


class VentanaPrincipal:
    """Ventana principal del simulador E-Waste."""

    def __init__(self, root: tk.Tk):
        self.root = root
        self._configurar_ventana()
        self._construir_ui()

    # ----------------------------------------------------------
    #  Configuracion de la ventana
    # ----------------------------------------------------------

    def _configurar_ventana(self):
        self.root.title("Simulador E-Waste | Scrap y Rezagos S.R.L.")
        self.root.geometry("1100x700")
        self.root.minsize(900, 600)
        self.root.configure(bg=COLORES["fondo"])
        # Centrar en pantalla
        self.root.update_idletasks()
        x = (self.root.winfo_screenwidth()  - 1100) // 2
        y = (self.root.winfo_screenheight() - 700)  // 2
        self.root.geometry(f"1100x700+{x}+{y}")

    # ----------------------------------------------------------
    #  Construccion de la UI
    # ----------------------------------------------------------

    def _construir_ui(self):
        self._barra_superior()
        self._contenido_bienvenida()
        self._barra_inferior()

    def _barra_superior(self):
        barra = tk.Frame(self.root, bg=COLORES["panel"], height=60)
        barra.pack(fill="x", side="top")
        barra.pack_propagate(False)

        titulo = tk.Label(
            barra,
            text="  Simulador E-Waste  |  Scrap y Rezagos S.R.L.",
            bg=COLORES["panel"],
            fg=COLORES["texto"],
            font=("Segoe UI", 14, "bold"),
            anchor="w",
        )
        titulo.pack(side="left", padx=16, pady=10)

        subtitulo = tk.Label(
            barra,
            text="UTN FRT - Simulacion - 4K2",
            bg=COLORES["panel"],
            fg=COLORES["subtexto"],
            font=("Segoe UI", 10),
        )
        subtitulo.pack(side="right", padx=20)

    def _contenido_bienvenida(self):
        frame = tk.Frame(self.root, bg=COLORES["fondo"])
        frame.pack(expand=True, fill="both", padx=40, pady=30)

        # Titulo central
        tk.Label(
            frame,
            text="Simulacion de Clasificacion de Residuos Electronicos",
            bg=COLORES["fondo"],
            fg=COLORES["texto"],
            font=("Segoe UI", 20, "bold"),
            wraplength=700,
            justify="center",
        ).pack(pady=(20, 8))

        tk.Label(
            frame,
            text="Modelado de eventos discretos con SimPy",
            bg=COLORES["fondo"],
            fg=COLORES["subtexto"],
            font=("Segoe UI", 12),
        ).pack(pady=(0, 30))

        # Tarjetas de canales
        self._tarjetas_canales(frame)

        # Boton principal
        btn = tk.Button(
            frame,
            text="  Iniciar Simulador  ",
            bg=COLORES["acento"],
            fg="white",
            font=("Segoe UI", 13, "bold"),
            relief="flat",
            cursor="hand2",
            padx=24,
            pady=10,
            command=self._abrir_simulador,
        )
        btn.pack(pady=30)

        btn.bind("<Enter>", lambda e: btn.config(bg=COLORES["acento_hover"]))
        btn.bind("<Leave>", lambda e: btn.config(bg=COLORES["acento"]))

    def _tarjetas_canales(self, parent):
        """Muestra los 3 canales de salida del sistema."""
        contenedor = tk.Frame(parent, bg=COLORES["fondo"])
        contenedor.pack()

        canales = [
            ("Reventa",   COLORES["rojo"],  "Dispositivos funcionales\ncon valor comercial"),
            ("Reciclaje", COLORES["verde"], "Desmantelamiento para\nrecuperacion de materiales"),
            ("Desecho",   COLORES["gris"],  "Disposicion final de\ncomponentes peligrosos"),
        ]

        for nombre, color, desc in canales:
            card = tk.Frame(
                contenedor,
                bg=COLORES["panel"],
                width=220,
                height=120,
                relief="flat",
                bd=0,
            )
            card.pack(side="left", padx=14, pady=4)
            card.pack_propagate(False)

            # Franja de color superior
            tk.Frame(card, bg=color, height=5).pack(fill="x")

            tk.Label(
                card,
                text=nombre,
                bg=COLORES["panel"],
                fg=color,
                font=("Segoe UI", 13, "bold"),
            ).pack(pady=(8, 2))

            tk.Label(
                card,
                text=desc,
                bg=COLORES["panel"],
                fg=COLORES["subtexto"],
                font=("Segoe UI", 9),
                justify="center",
            ).pack()

    def _barra_inferior(self):
        barra = tk.Frame(self.root, bg=COLORES["panel"], height=30)
        barra.pack(fill="x", side="bottom")
        barra.pack_propagate(False)

        tk.Label(
            barra,
            text="Grupo N1  |  Ammiraglia  -  Bazan  -  Figueroa  -  Lazarte  -  Moeykens  -  Munoz",
            bg=COLORES["panel"],
            fg=COLORES["subtexto"],
            font=("Segoe UI", 8),
        ).pack(expand=True)

    # ----------------------------------------------------------
    #  Acciones
    # ----------------------------------------------------------

    def _abrir_simulador(self):
        """Placeholder: en el proximo avance abre la pantalla de parametros."""
        ventana = tk.Toplevel(self.root)
        ventana.title("Proximamente...")
        ventana.geometry("400x150")
        ventana.configure(bg=COLORES["fondo"])
        tk.Label(
            ventana,
            text="Pantalla de parametros\nen construccion (Avance 2)",
            bg=COLORES["fondo"],
            fg=COLORES["texto"],
            font=("Segoe UI", 13),
        ).pack(expand=True)
