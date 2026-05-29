# ============================================================
#  panel_parametros.py  -  Columna IZQUIERDA
# ------------------------------------------------------------
#  AQUI VA: los controles que el usuario modifica antes de
#  simular (TEA, tamano de lote, operarios, error) y el boton
#  "Iniciar Simulacion".
#
#  RESPONSABILIDAD: leer lo que elige el usuario y entregarselo
#  al modelo de simulacion. NO ejecuta la simulacion en si.
# ============================================================

import tkinter as tk
from src.gui.tema import COLORES, FUENTES
from src.gui.componentes import titulo_panel, campo_parametro, campo_rango


class PanelParametros(tk.Frame):
    def __init__(self, parent, al_iniciar=None):
        super().__init__(parent, bg=COLORES["panel_param"], padx=14, pady=14)
        self.al_iniciar = al_iniciar   # funcion que se llama al apretar el boton
        self._construir()

    def _construir(self):
        titulo_panel(self, "PARAMETROS")

        # Cada campo devuelve una variable que luego leemos con .get()
        self.lotes_min, self.lotes_max = campo_rango(
            self, "Lotes por semana", range(3, 8), range(3, 8), 3, 7
        )
        self.lote      = campo_parametro(self, "Peso por lote (kg)",    [350, 400, 450, 500, 550], 450)
        self.operarios = campo_parametro(self, "Cantidad de Operarios", [3, 4, 5], 3)
        self.semanas   = campo_parametro(self, "Semanas de simulacion", [1, 2, 3, 4], 4)

        # Boton de accion
        btn = tk.Button(
            self, text="  Iniciar Simulacion", bg=COLORES["boton"],
            fg="white", font=FUENTES["boton"], relief="flat", cursor="hand2",
            pady=8, command=self._iniciar,
        )
        btn.pack(fill="x", pady=(20, 0))
        btn.bind("<Enter>", lambda e: btn.config(bg=COLORES["boton_hover"]))
        btn.bind("<Leave>", lambda e: btn.config(bg=COLORES["boton"]))

    def obtener_valores(self):
        """Devuelve un diccionario con lo que eligio el usuario."""
        return {
            "lotes_min": int(self.lotes_min.get()),
            "lotes_max": int(self.lotes_max.get()),
            "peso_lote": int(self.lote.get()),
            "operarios": int(self.operarios.get()),
            "semanas":   int(self.semanas.get()),
        }

    def _iniciar(self):
        if self.al_iniciar:
            self.al_iniciar(self.obtener_valores())
