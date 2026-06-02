# ============================================================
#  panel_resultados.py  -  Columna DERECHA
# ------------------------------------------------------------
#  AQUI VA: las metricas finales (total procesado, tiempo de
#  espera, rentabilidad) y los graficos de lineas.
#
#  RESPONSABILIDAD: MOSTRAR resultados. Recibe los datos ya
#  calculados desde la simulacion. Los graficos Matplotlib se
#  arman en src/graficos/ y se incrustan aqui.
# ============================================================

import tkinter as tk
from src.gui.tema import COLORES, FUENTES
from src.gui.componentes import titulo_panel, metrica


class PanelResultados(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent, bg=COLORES["panel_result"], padx=14, pady=14)
        self._construir()

    def _construir(self):
        titulo_panel(self, "RESULTADOS")

        self.lbl_total        = metrica(self, "TOTAL PROCESADOS", "0")
        self.lbl_prom_lote    = metrica(self, "PROMEDIO POR LOTE", "0")
        self.lbl_ocupacion    = metrica(self, "OCUPACION DEPOSITO", "0 %")
        self.lbl_espera       = metrica(self, "TIEMPO DE ESPERA EN COLA", "0 min.")
        self.lbl_rentabilidad = metrica(self, "RENTABILIDAD ESTIMADA", "$ 0")

        # --- Espacio reservado para los graficos ---
        # Aqui en el proximo avance se incrustan los canvas de Matplotlib
        # (tasa de arribos y ocupacion del deposito), generados desde
        # src/graficos/.
        self.contenedor_graficos = tk.Frame(self, bg=COLORES["panel_result"])
        self.contenedor_graficos.pack(fill="both", expand=True, pady=(14, 0))
        tk.Label(self.contenedor_graficos,
                 text="[ graficos: tasa de arribos\n y ocupacion deposito ]",
                 bg=COLORES["panel_result"], fg=COLORES["subtexto"],
                 font=FUENTES["texto_normal"]).pack(expand=True)

    def actualizar(self, total, espera_min, rentabilidad,
                   promedio_lote=0, ocupacion=0.0):
        """La simulacion llama a esto al terminar para mostrar los resultados."""
        self.lbl_total.config(text=f"{total:,}".replace(",", "."))
        self.lbl_prom_lote.config(text=f"{promedio_lote:,.0f}".replace(",", "."))
        # La ocupacion puede pasar de 100% (deposito desbordado): se avisa con color
        color_ocup = COLORES["venta"] if ocupacion > 0.9 else COLORES["texto"]
        self.lbl_ocupacion.config(text=f"{ocupacion:.0%}", fg=color_ocup)
        self.lbl_espera.config(text=f"{espera_min} min.")
        self.lbl_rentabilidad.config(text=f"$ {rentabilidad:,.0f}".replace(",", "."))
