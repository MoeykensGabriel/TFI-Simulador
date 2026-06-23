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
from tkinter import ttk
from src.gui.tema import COLORES, FUENTES
from src.gui.componentes import titulo_panel, tarjeta_canal


class PanelFlujo(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent, bg=COLORES["panel_centro"], padx=18, pady=16)
        self._construir()

    def _construir(self):
        titulo_panel(self, "FLUJO DE DISPOSITIVOS")

        # --- Aviso de estado (ej: "Simulando semana 1 de 4...") ---
        self.lbl_estado = tk.Label(
            self, text="Listo para simular",
            bg=COLORES["panel_centro"], fg=COLORES["texto"],
            font=FUENTES["valor_medio"],
        )
        self.lbl_estado.pack(pady=(4, 6))

        # --- Barra de progreso de semanas ---
        self.barra = ttk.Progressbar(
            self, style="Sim.Horizontal.TProgressbar",
            orient="horizontal", mode="determinate", length=320,
        )
        self.barra.pack(pady=(0, 4))

        # --- Etapas iniciales (entrada y clasificacion) ---
        fila = tk.Frame(self, bg=COLORES["panel_centro"])
        fila.pack(pady=14)

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

        # --- Card de ocupacion del deposito (cambia de color segun nivel) ---
        self._card_deposito(self)

    def _card_deposito(self, parent):
        """Card central con icono que muestra la ocupacion del deposito."""
        self.card_dep = tk.Frame(parent, bg=COLORES["reciclaje"], width=260, height=90)
        self.card_dep.pack(pady=(24, 0))
        self.card_dep.pack_propagate(False)

        # Icono + titulo en un renglon
        self.cabecera_dep = tk.Frame(self.card_dep, bg=COLORES["reciclaje"])
        self.cabecera_dep.pack(pady=(10, 0))
        self.lbl_dep_icono = tk.Label(self.cabecera_dep, text="\U0001F4E6", bg=COLORES["reciclaje"],
                                        fg="white", font=("Segoe UI Emoji", 16))
        self.lbl_dep_icono.pack(side="left", padx=(0, 6))
        self.lbl_dep_titulo = tk.Label(self.cabecera_dep, text="OCUPACION DEPOSITO",
                                        bg=COLORES["reciclaje"], fg="white",
                                        font=FUENTES["texto_normal"])
        self.lbl_dep_titulo.pack(side="left")

        # Porcentaje grande
        self.lbl_dep_valor = tk.Label(self.card_dep, text="0%", bg=COLORES["reciclaje"],
                                        fg="white", font=FUENTES["valor_grande"])
        self.lbl_dep_valor.pack()

    def _etapa(self, parent, nombre, valor):
        """Caja blanca con nombre de etapa y un numero grande."""
        caja = tk.Frame(parent, bg=COLORES["tarjeta"], width=140, height=112,
                        highlightbackground=COLORES["borde"], highlightthickness=1)
        caja.pack(side="left", padx=18)
        caja.pack_propagate(False)
        tk.Label(caja, text=nombre, bg=COLORES["tarjeta"], fg=COLORES["subtexto"],
                    font=FUENTES["texto_normal"]).pack(pady=(16, 4))
        lbl = tk.Label(caja, text=valor, bg=COLORES["tarjeta"], fg=COLORES["acento"],
                        font=FUENTES["valor_grande"])
        lbl.pack()
        return lbl

    def actualizar_progreso(self, semana, total):
        """Mueve la barra de progreso segun la semana actual."""
        self.barra["maximum"] = total
        self.barra["value"] = semana

    def actualizar(self, entrada, clasificados, venta, reciclaje, desecho):
        """La simulacion llama a esto para refrescar los numeros en pantalla."""
        self.lbl_entrada.config(text=str(entrada))
        self.lbl_clasif.config(text=str(clasificados))
        self.lbl_venta.config(text=str(venta))
        self.lbl_reciclaje.config(text=str(reciclaje))
        self.lbl_desecho.config(text=str(desecho))

    def actualizar_estado(self, texto, color=None):
        """Refresca el aviso de estado (ej: 'Simulando semana 2 de 4...')."""
        self.lbl_estado.config(text=texto, fg=color or COLORES["texto"])

    def actualizar_deposito(self, ocupacion):
        """
        Refresca la card de ocupacion del deposito y la pinta segun el nivel:
        verde   < 70%   (holgado)
        naranja 70-90%  (cargado)
        rojo    > 90%   (desbordado -> dispara Alternativa A)
        """
        if ocupacion < 0.70:
            color = COLORES["ok"]          # verde
        elif ocupacion <= 0.90:
            color = COLORES["alerta"]      # naranja
        else:
            color = COLORES["peligro"]     # rojo

        # Repintar todos los elementos de la card (incluida la cabecera)
        for w in (self.card_dep, self.cabecera_dep, self.lbl_dep_icono,
                    self.lbl_dep_titulo, self.lbl_dep_valor):
            w.config(bg=color)
        self.lbl_dep_valor.config(text=f"{ocupacion:.0%}")
