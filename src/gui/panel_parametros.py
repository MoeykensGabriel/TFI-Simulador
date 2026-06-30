# ============================================================
#  panel_parametros.py  -  Columna IZQUIERDA
# ------------------------------------------------------------
#  AQUI VA: los controles que el usuario modifica antes de
#  simular y el boton "Iniciar Simulacion".
#
#  RESPONSABILIDAD: leer lo que elige el usuario y entregarselo
#  al modelo de simulacion. NO ejecuta la simulacion en si.
# ============================================================

import tkinter as tk
from tkinter import ttk
from src.gui.tema import COLORES, FUENTES
from src.gui.componentes import titulo_panel, campo_parametro, campo_rango


# Precios en miles de ARS para que quepan en el dropdown
PRECIOS_CEL_MIN = [100, 125, 150, 175, 200]   # x1000 ARS
PRECIOS_CEL_MAX = [300, 325, 350, 375, 400]
PRECIOS_TAB_MIN = [200, 225, 250, 275, 300]
PRECIOS_TAB_MAX = [450, 500, 550, 600]
MARGENES        = [5, 10, 15, 20, 25]         # %
SALARIOS        = [800, 900, 1000, 1100, 1200] # x1000 ARS


class PanelParametros(tk.Frame):
    def __init__(self, parent, al_iniciar=None):
        super().__init__(parent, bg=COLORES["panel_param"])
        self.al_iniciar = al_iniciar
        self._construir_scroll()

    def _construir_scroll(self):
        """Envuelve el contenido en un Canvas con scrollbar vertical."""
        # Canvas que actua como viewport
        canvas = tk.Canvas(self, bg=COLORES["panel_param"], highlightthickness=0)
        scrollbar = ttk.Scrollbar(self, orient="vertical", command=canvas.yview)
        canvas.configure(yscrollcommand=scrollbar.set)

        scrollbar.pack(side="right", fill="y")
        canvas.pack(side="left", fill="both", expand=True)

        # Frame interior que contiene todos los campos
        self.interior = tk.Frame(canvas, bg=COLORES["panel_param"], padx=14, pady=10)
        ventana_id = canvas.create_window((0, 0), window=self.interior, anchor="nw")

        # Ajustar el scrollregion cuando cambia el tamaño del interior
        def _actualizar_scroll(e):
            canvas.configure(scrollregion=canvas.bbox("all"))

        def _ajustar_ancho(e):
            canvas.itemconfig(ventana_id, width=e.width)

        self.interior.bind("<Configure>", _actualizar_scroll)
        canvas.bind("<Configure>", _ajustar_ancho)

        # Scroll con la rueda del mouse
        canvas.bind_all("<MouseWheel>", lambda e: canvas.yview_scroll(
            int(-1 * (e.delta / 120)), "units"
        ))

        self._construir(self.interior)

    def _construir(self, parent):
        titulo_panel(parent, "PARAMETROS")

        # --- Lotes por semana (Min / Max en el mismo renglon) ---
        self.lotes_min, self.lotes_max = campo_rango(
            parent, "Lotes por semana", range(3, 8), range(3, 8), 3, 7
        )

        # --- Tamano de lote (Media / Desviacion en el mismo renglon) ---
        self.lote_media, self.lote_desv = campo_rango(
            parent, "Tamano de lote (kg)", [350, 400, 450, 500, 550], [50, 75, 100, 125, 150], 450, 100
        )

        # --- Precio celular ARS (Min / Max) ---
        self.cel_min, self.cel_max = campo_rango(
            parent, "Precio celular (miles $)", PRECIOS_CEL_MIN, PRECIOS_CEL_MAX, 150, 350
        )

        # --- Precio tablet ARS (Min / Max) ---
        self.tab_min, self.tab_max = campo_rango(
            parent, "Precio tablet (miles $)", PRECIOS_TAB_MIN, PRECIOS_TAB_MAX, 250, 550
        )

        # --- Margen de rentabilidad ---
        self.margen    = campo_parametro(parent, "Margen de rentabilidad (%)", MARGENES, 15)

        # --- Cantidad de operarios ---
        self.operarios = campo_parametro(parent, "Cantidad de operarios", range(3,10), 3)

        # --- Salario tecnico ---
        self.salario   = campo_parametro(parent, "Salario tecnico (miles $)", SALARIOS, 1100)

        # --- Semanas de simulacion (4 a 12) ---
        self.semanas   = campo_parametro(parent, "Semanas de simulacion", range(4, 13), 4)

        # --- Boton iniciar ---
        self.btn_simular = btn = tk.Button(
            parent, text="▶  Iniciar Simulacion", bg=COLORES["boton"],
            fg="white", font=FUENTES["boton"], relief="flat", cursor="hand2",
            activebackground=COLORES["boton_hover"], activeforeground="white",
            bd=0, pady=11, command=self._iniciar,
        )
        btn.pack(fill="x", pady=(18, 6))
        btn.bind("<Enter>", lambda e: btn.config(bg=self._color_hover()))
        btn.bind("<Leave>", lambda e: btn.config(bg=self._color_base()))

    def _corriendo(self):
        return "Detener" in self.btn_simular["text"]

    def _color_base(self):
        return COLORES["boton_stop"] if self._corriendo() else COLORES["boton"]

    def _color_hover(self):
        return COLORES["boton_stop_hover"] if self._corriendo() else COLORES["boton_hover"]

    def obtener_valores(self):
        """Devuelve un diccionario con todos los valores elegidos por el usuario."""
        return {
            "lotes_min":      int(self.lotes_min.get()),
            "lotes_max":      int(self.lotes_max.get()),
            "lote_media":     int(self.lote_media.get()),
            "lote_desv":      int(self.lote_desv.get()),
            "cel_precio_min": int(self.cel_min.get()) * 1000,
            "cel_precio_max": int(self.cel_max.get()) * 1000,
            "tab_precio_min": int(self.tab_min.get()) * 1000,
            "tab_precio_max": int(self.tab_max.get()) * 1000,
            "margen":         int(self.margen.get()),
            "operarios":      int(self.operarios.get()),
            "salario":        int(self.salario.get()) * 1000,
            "semanas":        int(self.semanas.get()),
        }

    def resetear_boton(self):
        """Vuelve el boton a 'Iniciar' cuando la simulacion termina sola."""
        self.btn_simular.config(text="▶  Iniciar Simulacion", bg=COLORES["boton"])

    def estado(self):
        """Devuelve las selecciones crudas (para restaurarlas al cambiar de tema)."""
        return {
            "lotes_min": self.lotes_min.get(), "lotes_max": self.lotes_max.get(),
            "lote_media": self.lote_media.get(), "lote_desv": self.lote_desv.get(),
            "cel_min": self.cel_min.get(), "cel_max": self.cel_max.get(),
            "tab_min": self.tab_min.get(), "tab_max": self.tab_max.get(),
            "margen": self.margen.get(), "operarios": self.operarios.get(),
            "salario": self.salario.get(), "semanas": self.semanas.get(),
        }

    def restaurar(self, e):
        """Re-aplica selecciones guardadas con estado()."""
        try:
            self.lotes_min.set(e["lotes_min"]); self.lotes_max.set(e["lotes_max"])
            self.lote_media.set(e["lote_media"]); self.lote_desv.set(e["lote_desv"])
            self.cel_min.set(e["cel_min"]); self.cel_max.set(e["cel_max"])
            self.tab_min.set(e["tab_min"]); self.tab_max.set(e["tab_max"])
            self.margen.set(e["margen"]); self.operarios.set(e["operarios"])
            self.salario.set(e["salario"]); self.semanas.set(e["semanas"])
        except Exception:
            pass

    def _iniciar(self):
        if self.al_iniciar:
            if self.al_iniciar(self.obtener_valores()):
                self.btn_simular.config(text="■  Detener Simulacion", bg=COLORES["boton_stop"])
            else:
                self.btn_simular.config(text="▶  Iniciar Simulacion", bg=COLORES["boton"])