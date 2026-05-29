# ============================================================
#  panel_flujo.py  -  Columna CENTRAL
# ------------------------------------------------------------
#  AQUI VA: la representacion visual del proceso:
#  Entrada de lote -> Clasificacion -> 3 canales de salida.
#
#  RESPONSABILIDAD: MOSTRAR el estado del sistema. Recibe numeros
#  desde la simulacion (cuantos entraron, cuantos a cada canal)
#  y los dibuja. NO calcula nada por su cuenta.
# ============================================================

import tkinter as tk
from src.gui.tema import COLORES, FUENTES
from src.gui.componentes import titulo_panel, tarjeta_canal


class PanelFlujo(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent, bg=COLORES["panel_centro"], padx=14, pady=14)
        self._construir()

    def _construir(self):
        titulo_panel(self, "FLUJO DE DISPOSITIVOS")

        # --- Etapas iniciales (entrada y clasificacion) ---
        fila = tk.Frame(self, bg=COLORES["panel_centro"])
        fila.pack(pady=20)

        self.lbl_entrada = self._etapa(fila, "ENTRADA\nDE LOTE", "0")
        self.lbl_clasif  = self._etapa(fila, "CLASIFICACION", "0")

        # --- Canales de salida ---
        canales = tk.Frame(self, bg=COLORES["panel_centro"])
        canales.pack(pady=10)

        _, self.lbl_venta     = tarjeta_canal(canales, "VENTA",     COLORES["venta"])
        _, self.lbl_reciclaje = tarjeta_canal(canales, "RECICLAJE", COLORES["reciclaje"])
        _, self.lbl_desecho   = tarjeta_canal(canales, "DESECHO",   COLORES["desecho"])
        for w in canales.winfo_children():
            w.pack(side="left", padx=8)

    def _etapa(self, parent, nombre, valor):
        """Caja blanca con nombre de etapa y un numero grande."""
        caja = tk.Frame(parent, bg=COLORES["tarjeta"], width=130, height=110)
        caja.pack(side="left", padx=18)
        caja.pack_propagate(False)
        tk.Label(caja, text=nombre, bg=COLORES["tarjeta"], fg=COLORES["texto"],
                 font=FUENTES["texto_normal"]).pack(pady=(10, 4))
        lbl = tk.Label(caja, text=valor, bg=COLORES["tarjeta"], fg=COLORES["texto"],
                       font=FUENTES["valor_grande"])
        lbl.pack()
        return lbl

    def actualizar(self, entrada, clasificados, venta, reciclaje, desecho):
        """La simulacion llama a esto para refrescar los numeros en pantalla."""
        self.lbl_entrada.config(text=str(entrada))
        self.lbl_clasif.config(text=str(clasificados))
        self.lbl_venta.config(text=str(venta))
        self.lbl_reciclaje.config(text=str(reciclaje))
        self.lbl_desecho.config(text=str(desecho))
