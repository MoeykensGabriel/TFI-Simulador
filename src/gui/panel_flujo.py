# panel_flujo.py - columna central: diagrama animado del proceso
# entrada de lote -> clasificacion -> uno de los tres canales

import random as _anim_rng   # solo para la animacion (cosmetico, no el modelo)
import tkinter as tk
from tkinter import ttk
from src.gui.tema import COLORES, FUENTES
from src.gui.componentes import titulo_panel


# medidas del lienzo del diagrama
_CW, _CH = 560, 380


class PanelFlujo(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent, bg=COLORES["panel_centro"], padx=18, pady=16)
        self._dispositivos = []   # iconos en vuelo
        self._construir()

    def _construir(self):
        titulo_panel(self, "FLUJO DE DISPOSITIVOS")

        self.lbl_estado = tk.Label(
            self, text="Listo para simular",
            bg=COLORES["panel_centro"], fg=COLORES["texto"],
            font=FUENTES["valor_medio"],
        )
        self.lbl_estado.pack(pady=(4, 6))

        self.barra = ttk.Progressbar(
            self, style="Sim.Horizontal.TProgressbar",
            orient="horizontal", mode="determinate", length=320,
        )
        self.barra.pack(pady=(0, 8))

        # --- Lienzo del diagrama ---
        self.canvas = tk.Canvas(self, width=_CW, height=_CH,
                                bg=COLORES["panel_centro"], highlightthickness=0)
        self.canvas.pack()

        # posiciones (centros) de cada nodo del diagrama
        self.nodos = {
            "entrada":   (_CW / 2, 46),
            "clasif":    (_CW / 2, 168),
            "venta":     (112, 308),
            "reciclaje": (_CW / 2, 308),
            "desecho":   (448, 308),
        }

        self._dibujar_conexiones()
        self.txt = {}
        self.txt["entrada"]   = self._nodo("entrada",   "ENTRADA DE LOTE", "0",
                                            COLORES["tarjeta"], COLORES["acento"], COLORES["subtexto"])
        self.txt["clasif"]    = self._nodo("clasif",    "CLASIFICACION", "0",
                                            COLORES["tarjeta"], COLORES["acento"], COLORES["subtexto"])
        self.txt["venta"]     = self._nodo("venta",     "VENTA", "0",
                                            COLORES["venta"], "white", "white")
        self.txt["reciclaje"] = self._nodo("reciclaje", "RECICLAJE", "0",
                                            COLORES["reciclaje"], "white", "white")
        self.txt["desecho"]   = self._nodo("desecho",   "DESECHO", "0",
                                            COLORES["desecho"], "white", "white")

        # --- Card de ocupacion del deposito ---
        self._card_deposito(self)

    def _dibujar_conexiones(self):
        """Lineas guia entrada -> clasif -> cada canal (van detras de los nodos)."""
        ex, ey = self.nodos["entrada"]
        cx, cy = self.nodos["clasif"]
        self.canvas.create_line(ex, ey + 26, cx, cy - 26,
                                fill=COLORES["borde"], width=2, arrow="last")
        for canal in ("venta", "reciclaje", "desecho"):
            kx, ky = self.nodos[canal]
            self.canvas.create_line(cx, cy + 26, kx, ky - 30,
                                    fill=COLORES["borde"], width=2, arrow="last")

    def _nodo(self, clave, titulo, valor, fill, fg, titulo_fg):
        """Dibuja una caja con titulo y valor; devuelve el id del texto del valor."""
        cx, cy = self.nodos[clave]
        w, h = (150, 58) if clave in ("entrada", "clasif") else (134, 64)
        self.canvas.create_rectangle(cx - w / 2, cy - h / 2, cx + w / 2, cy + h / 2,
                                     fill=fill, outline=COLORES["borde"], width=1)
        self.canvas.create_text(cx, cy - 14, text=titulo, fill=titulo_fg,
                                font=FUENTES["texto_normal"])
        return self.canvas.create_text(cx, cy + 10, text=valor, fill=fg,
                                       font=FUENTES["valor_medio"])

    # ----------------------------------------------------------
    #  Animacion de dispositivos
    # ----------------------------------------------------------
    def animar_semana(self, conteos, cantidad=8):
        """Lanza varios iconos que recorren el flujo durante la semana.
        El canal de cada uno se elige al azar segun los conteos reales."""
        total = sum(conteos) or 1
        pesos = [c / total for c in conteos]
        canales = ("venta", "reciclaje", "desecho")
        for k in range(cantidad):
            destino = self._elegir(canales, pesos)
            self.after(k * 230, lambda c=destino: self._lanzar(c))

    def _elegir(self, canales, pesos):
        u = _anim_rng.random()
        acum = 0.0
        for canal, peso in zip(canales, pesos):
            acum += peso
            if u <= acum:
                return canal
        return canales[-1]

    def _lanzar(self, canal):
        """Crea un celular en ENTRADA y lo mueve: entrada -> clasif -> canal."""
        ex, ey = self.nodos["entrada"]
        icono = self.canvas.create_text(ex, ey - 2, text="\U0001F4F1",
                                        font=("Segoe UI Emoji", 16))
        self._dispositivos.append(icono)

        cx, cy = self.nodos["clasif"]
        kx, ky = self.nodos[canal]

        def a_canal():
            self.canvas.itemconfig(icono, fill=COLORES[canal])
            self._mover(icono, cx, cy, kx, ky, 22, lambda: self._llegada(icono))

        self._mover(icono, ex, ey, cx, cy, 22, a_canal)

    def _mover(self, item, x0, y0, x1, y1, pasos, al_terminar):
        """Tween simple: mueve un item de (x0,y0) a (x1,y1) en N pasos."""
        dx = (x1 - x0) / pasos
        dy = (y1 - y0) / pasos

        def paso(i):
            if item not in self._dispositivos:
                return
            if i >= pasos:
                self.canvas.coords(item, x1, y1)
                if al_terminar:
                    al_terminar()
                return
            self.canvas.move(item, dx, dy)
            self.after(16, lambda: paso(i + 1))

        paso(0)

    def _llegada(self, icono):
        """Al llegar al canal, espera un instante y desaparece."""
        def borrar():
            if icono in self._dispositivos:
                self._dispositivos.remove(icono)
                self.canvas.delete(icono)
        self.after(350, borrar)

    def limpiar_animacion(self):
        """Borra los iconos en vuelo (al reiniciar una simulacion)."""
        for icono in self._dispositivos:
            self.canvas.delete(icono)
        self._dispositivos = []

    # ----------------------------------------------------------
    #  Deposito
    # ----------------------------------------------------------
    def _card_deposito(self, parent):
        self.card_dep = tk.Frame(parent, bg=COLORES["ok"], width=270, height=84)
        self.card_dep.pack(pady=(12, 0))
        self.card_dep.pack_propagate(False)

        self.cabecera_dep = tk.Frame(self.card_dep, bg=COLORES["ok"])
        self.cabecera_dep.pack(pady=(12, 0))
        self.lbl_dep_icono = tk.Label(self.cabecera_dep, text="\U0001F4E6", bg=COLORES["ok"],
                                      fg="white", font=("Segoe UI Emoji", 16))
        self.lbl_dep_icono.pack(side="left", padx=(0, 6))
        self.lbl_dep_titulo = tk.Label(self.cabecera_dep, text="OCUPACION DEPOSITO",
                                       bg=COLORES["ok"], fg="white",
                                       font=FUENTES["texto_normal"])
        self.lbl_dep_titulo.pack(side="left")

        self.lbl_dep_valor = tk.Label(self.card_dep, text="0%", bg=COLORES["ok"],
                                      fg="white", font=FUENTES["valor_grande"])
        self.lbl_dep_valor.pack()

    # ----------------------------------------------------------
    #  Actualizaciones que llama la simulacion
    # ----------------------------------------------------------
    def actualizar(self, entrada, clasificados, venta, reciclaje, desecho):
        self.canvas.itemconfig(self.txt["entrada"],   text=str(entrada))
        self.canvas.itemconfig(self.txt["clasif"],    text=str(clasificados))
        self.canvas.itemconfig(self.txt["venta"],     text=str(venta))
        self.canvas.itemconfig(self.txt["reciclaje"], text=str(reciclaje))
        self.canvas.itemconfig(self.txt["desecho"],   text=str(desecho))

    def actualizar_estado(self, texto, color=None):
        self.lbl_estado.config(text=texto, fg=color or COLORES["texto"])

    def actualizar_progreso(self, semana, total):
        self.barra["maximum"] = total
        self.barra["value"] = semana

    def actualizar_deposito(self, ocupacion):
        """Pinta la card segun el nivel: verde <70%, naranja 70-90%, rojo >90%."""
        if ocupacion < 0.70:
            color = COLORES["ok"]
        elif ocupacion <= 0.90:
            color = COLORES["alerta"]
        else:
            color = COLORES["peligro"]
        for w in (self.card_dep, self.cabecera_dep, self.lbl_dep_icono,
                  self.lbl_dep_titulo, self.lbl_dep_valor):
            w.config(bg=color)
        self.lbl_dep_valor.config(text=f"{ocupacion:.0%}")
