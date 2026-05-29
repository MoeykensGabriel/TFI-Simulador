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
from src.gui.componentes import titulo_panel, campo_parametro


class PanelParametros(tk.Frame):
    def __init__(self, parent, al_iniciar=None):
        super().__init__(parent, bg=COLORES["panel_param"], padx=14, pady=14)
        self.al_iniciar = al_iniciar   # funcion que se llama al apretar el boton
        self._construir()

    def _construir(self):
        titulo_panel(self, "PARAMETROS")

        # Cada campo devuelve una variable que luego leemos con .get()
        self.tea       = campo_parametro(self, "TEA Promedio",         [4, 5, 6, 7, 8], 6)
        self.lote      = campo_parametro(self, "Tamano de Lote",       [100, 150, 200, 250], 200)
        self.operarios = campo_parametro(self, "Cantidad de Operarios", [3, 4, 5], 5)
        self.error     = campo_parametro(self, "Error de Clasificacion", ["2 %", "3 %", "4 %", "5 %"], "3 %")

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
            "tea":       int(self.tea.get()),
            "lote":      int(self.lote.get()),
            "operarios": int(self.operarios.get()),
            "error":     int(self.error.get().replace("%", "").strip()),
        }

    def _iniciar(self):
        if self.al_iniciar:
            self.al_iniciar(self.obtener_valores())
