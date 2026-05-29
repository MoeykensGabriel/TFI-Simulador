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
        self.lotes_A, self.lotes_B = campo_rango(self, "Lotes semanales", "Mínimo", "Máximo", range(1, 10), range(1, 10), 3, 7)
        self.lote_PROM, self.lote_DES = campo_rango(self, "Tamano de Lote", "Promedio", "+-", [100, 150, 200, 250], [100, 150, 200, 250], 200, 250)
        self.operarios = campo_parametro(self, "Cantidad de Operarios", [3, 4], 3)
        self.error = campo_parametro(self, "Error de Clasificacion", ["2 %", "3 %", "4 %", "5 %"], "3 %")
        self.ventalcel_A, self.ventalcel_B = campo_rango(self, "Precio de venta de celulares", "Mínimo", "Máximo", range(1, 10), range(1, 10), 1, 7)
        self.ventaltablets_A, self.ventaltablets_B = campo_rango(self, "Precio de venta de tablets", "Mínimo", "Máximo", range(1, 10), range(1, 10), 1, 7)
        self.margen = campo_parametro(self, "Margen de rentabilidad", range(1, 10), 1)
        self.salarios = campo_parametro(self, "Salarios de un técnico", range(1, 10), 10)
        self.semanas = campo_parametro(self, "Semanas de Simulacion",range(4, 13), 4)

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
            "lotes_A":   int(self.lotes_A.get()),
            "lotes_B":   int(self.lotes_B.get()),
            "lote_PROM": int(self.lote_PROM.get()),
            "lote_DES":  int(self.lote_DES.get()),
            "operarios": int(self.operarios.get()),
            "error":     int(self.error.get().replace("%", "").strip()),
            "ventalcel_A": int(self.ventalcel_A.get()),
            "ventalcel_B": int(self.ventalcel_B.get()),
            "ventaltablets_A": int(self.ventaltablets_A.get()),
            "ventaltablets_B": int(self.ventaltablets_B.get()),
            "margen": int(self.margen.get()),
            "salarios": int(self.salarios.get()),
            "semanas":   int(self.semanas.get()),
        }

    def _iniciar(self):
        if self.al_iniciar:
            self.al_iniciar(self.obtener_valores())
