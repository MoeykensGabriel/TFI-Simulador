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
    def __init__(self, parent, al_ver_recomendaciones=None):
        super().__init__(parent, bg=COLORES["panel_result"], padx=14, pady=14)
        self.al_ver_recomendaciones = al_ver_recomendaciones
        self._construir()

    def _construir(self):
        titulo_panel(self, "RESULTADOS")

        self.lbl_total        = metrica(self, "TOTAL PROCESADOS", "0")
        self.lbl_prom_lote    = metrica(self, "PROMEDIO POR LOTE", "0")
        self.lbl_espera       = metrica(self, "TIEMPO DE ESPERA EN COLA", "0 min.")
        self.lbl_rentabilidad = metrica(self, "RENTABILIDAD ESTIMADA", "$ 0")

        # --- Boton de recomendaciones (oculto hasta terminar la simulacion) ---
        self.btn_recom = tk.Button(
            self, text="📋  Ver Recomendaciones", bg=COLORES["boton"],
            fg="white", font=FUENTES["boton"], relief="flat", cursor="hand2",
            activebackground=COLORES["boton_hover"], activeforeground="white",
            bd=0, pady=11, command=self._click_recomendaciones,
        )
        self.btn_recom.bind("<Enter>", lambda e: self.btn_recom.config(bg=COLORES["boton_hover"]))
        self.btn_recom.bind("<Leave>", lambda e: self.btn_recom.config(bg=COLORES["boton"]))
        # No se hace pack() todavia: aparece solo al finalizar

        # --- Espacio reservado para los graficos ---
        self.contenedor_graficos = tk.Frame(
            self, bg=COLORES["superficie_alt"],
            highlightbackground=COLORES["borde"], highlightthickness=1)
        self.contenedor_graficos.pack(fill="both", expand=True, pady=(16, 0))
        tk.Label(self.contenedor_graficos,
                    text="📊\n\ngraficos de arribos\ny ocupacion del deposito",
                    bg=COLORES["superficie_alt"], fg=COLORES["subtexto"],
                    font=FUENTES["texto_normal"], justify="center").pack(expand=True)

    def actualizar(self, total, espera_min, rentabilidad, promedio_lote=0):
        """La simulacion llama a esto al terminar para mostrar los resultados."""
        self.lbl_total.config(text=f"{total:,}".replace(",", "."))
        self.lbl_prom_lote.config(text=f"{promedio_lote:,.0f}".replace(",", "."))
        self.lbl_espera.config(text=f"{espera_min} min.")
        self.lbl_rentabilidad.config(text=f"$ {rentabilidad:,.0f}".replace(",", "."))

    def mostrar_boton_recomendaciones(self):
        self.btn_recom.pack(fill="x", pady=(20, 0))

    def esconder_boton_recomendaciones(self):
        self.btn_recom.pack_forget()

    def _click_recomendaciones(self):
        if self.al_ver_recomendaciones:
            self.al_ver_recomendaciones()
