# ============================================================
#  ventana_principal.py  -  Ventana raiz / ensamblador
# ------------------------------------------------------------
#  AQUI VA: el armado general de la ventana. Crea el header y
#  coloca los 3 paneles (parametros | flujo | resultados).
#
#  RESPONSABILIDAD: ORQUESTAR. Conecta el boton "Iniciar" del
#  panel de parametros con la simulacion, y reparte los
#  resultados a los paneles de flujo y resultados.
#  NO contiene detalles visuales de cada columna (eso vive en
#  cada panel_*.py).
# ============================================================

import tkinter as tk
from src.gui.tema import COLORES, FUENTES, MEDIDAS
from src.gui.panel_parametros import PanelParametros
from src.gui.panel_flujo import PanelFlujo
from src.gui.panel_resultados import PanelResultados
from src.gui.ventana_recomendaciones import VentanaRecomendaciones
from src.simulacion.parametros import Parametros
from src.simulacion.modelo import ModeloSimulacion
from src.simulacion.alternativas import evaluar_alternativas


class VentanaPrincipal:
    def __init__(self, root: tk.Tk):
        self.root = root
        self._configurar_ventana()
        self._header()
        self._cuerpo()

    def _configurar_ventana(self):
        self.root.title("Simulador de Clasificacion de RAEE | Scrap y Rezagos S.R.L.")
        ancho, alto = MEDIDAS["ancho_ventana"], MEDIDAS["alto_ventana"]
        self.root.configure(bg=COLORES["fondo"])
        self.root.update_idletasks()
        x = (self.root.winfo_screenwidth()  - ancho) // 2
        y = (self.root.winfo_screenheight() - alto)  // 2
        self.root.geometry(f"{ancho}x{alto}+{x}+{y}")
        self.root.minsize(1100, 620)

    def _header(self):
        barra = tk.Frame(self.root, bg=COLORES["header"], height=60)
        barra.pack(fill="x")
        barra.pack_propagate(False)
        tk.Label(barra, text="SIMULADOR DE CLASIFICACION DE RAEE",
        bg=COLORES["header"], fg=COLORES["texto_claro"],
        font=FUENTES["titulo_app"]).pack(side="left", padx=20, pady=8)
        tk.Label(barra, text="Scrap & Rezagos S.R.L.",
        bg=COLORES["header"], fg=COLORES["texto_claro"],
        font=FUENTES["valor_medio"]).pack(side="right", padx=20)

    def _cuerpo(self):
        cuerpo = tk.Frame(self.root, bg=COLORES["fondo"])
        cuerpo.pack(fill="both", expand=True, padx=10, pady=10)

        # Columna izquierda (ancho fijo)
        self.panel_param = PanelParametros(cuerpo, al_iniciar=self._ejecutar_simulacion)
        self.panel_param.pack(side="left", fill="y")
        self.panel_param.configure(width=MEDIDAS["ancho_param"])
        self.panel_param.pack_propagate(False)

        # Columna central (se estira)
        self.panel_flujo = PanelFlujo(cuerpo)
        self.panel_flujo.pack(side="left", fill="both", expand=True, padx=10)

        # Columna derecha (ancho fijo)
        self.panel_result = PanelResultados(cuerpo, al_ver_recomendaciones=self._abrir_recomendaciones)
        self.panel_result.pack(side="left", fill="y")
        self.panel_result.configure(width=MEDIDAS["ancho_result"])
        self.panel_result.pack_propagate(False)

    # ----------------------------------------------------------
    #  Conexion GUI <-> simulacion
    # ----------------------------------------------------------
    # Milisegundos de pausa entre una semana y la siguiente
    PAUSA_SEMANA = 3000
    # Cada cuanto parpadean los puntos de la animacion
    PAUSA_PUNTOS = 400

    def _ejecutar_simulacion(self, valores):
        """
        Se llama al apretar 'Iniciar Simulacion'.
        Arranca la simulacion en modo 'semana a semana': procesa una
        semana, refresca la pantalla, y agenda la siguiente con 3
        segundos de pausa para que se vea el avance en tiempo real.
        """
        p = Parametros.desde_gui(valores)
        self.modelo = ModeloSimulacion(p)
        self.total_semanas = p.semanas_simulacion
        self.semana_actual = 1
        self.simulando = True
        self._puntos = 0
        self._animar_puntos()      # arranca la animacion de puntos
        self._procesar_semana()

    def _animar_puntos(self):
        """Hace parpadear los puntos del aviso (. .. ...) mientras simula."""
        if not self.simulando:
            return
        self._puntos = (self._puntos + 1) % 4
        texto = f"Simulando semana {self.semana_actual} de {self.total_semanas}"
        self.panel_flujo.actualizar_estado(
            texto + "." * self._puntos, color=COLORES["boton"]
        )
        self.root.after(self.PAUSA_PUNTOS, self._animar_puntos)

    def _procesar_semana(self):
        """Procesa una semana, actualiza los paneles y agenda la siguiente."""
        r = self.modelo.correr_semana()   # acumula una semana mas

        # Refrescar el panel central con los acumulados hasta ahora
        self.panel_flujo.actualizar(
            entrada=r.total_procesados,
            clasificados=r.total_procesados,
            venta=r.a_venta,
            reciclaje=r.a_reciclaje,
            desecho=r.a_desecho,
        )

        # Refrescar metricas (la espera/ocupacion se calculan al final)
        self.panel_result.actualizar(
            total=r.total_procesados,
            espera_min=round(r.wq_min),
            rentabilidad=r.ganancia_neta,
            promedio_lote=r.promedio_por_lote,
        )

        # Si era la ultima semana, terminar
        if self.semana_actual >= self.total_semanas:
            self.simulando = False
            # Correr la teoria de colas (M/M/c) y refrescar espera + ocupacion
            self.modelo.calcular_colas()
            self.panel_result.actualizar(
                total=r.total_procesados,
                espera_min=round(r.wq_min),
                rentabilidad=r.ganancia_neta,
                promedio_lote=r.promedio_por_lote,
            )
            self.panel_flujo.actualizar_deposito(r.ocupacion_deposito)
            self.panel_flujo.actualizar_estado(
                f"Simulacion finalizada ({self.total_semanas} semanas)",
                color=COLORES["reciclaje"],
            )
            # Evaluar las 4 alternativas y habilitar el boton de recomendaciones
            self.alternativas = evaluar_alternativas(r, self.modelo.p)
            self.panel_result.mostrar_boton_recomendaciones()
            return

        # Agendar la proxima semana: esperar 3s y recien ahi avanzar
        def siguiente():
            self.semana_actual += 1
            self._procesar_semana()

        self.root.after(self.PAUSA_SEMANA, siguiente)

    def _abrir_recomendaciones(self):
        """Abre la ventana con el diagnostico de las 4 alternativas."""
        if hasattr(self, "alternativas"):
            VentanaRecomendaciones(self.root, self.alternativas)
