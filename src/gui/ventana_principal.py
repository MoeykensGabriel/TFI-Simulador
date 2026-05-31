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
from src.simulacion.parametros import Parametros
from src.simulacion.modelo import ModeloSimulacion


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
        self.panel_result = PanelResultados(cuerpo)
        self.panel_result.pack(side="left", fill="y")
        self.panel_result.configure(width=MEDIDAS["ancho_result"])
        self.panel_result.pack_propagate(False)

    # ----------------------------------------------------------
    #  Conexion GUI <-> simulacion
    # ----------------------------------------------------------
    def _ejecutar_simulacion(self, valores):
        """
        Se llama al apretar 'Iniciar Simulacion'.
        Crea los parametros desde la GUI, corre el modelo y reparte
        los resultados a los paneles de flujo y resultados.
        """
        # 1) Construir parametros con lo elegido por el usuario
        p = Parametros.desde_gui(valores)

        # 2) Correr la simulacion
        resultados = ModeloSimulacion(p).correr()

        # 3) Mostrar los conteos en el panel central (flujo)
        self.panel_flujo.actualizar(
            entrada=resultados.total_procesados,
            clasificados=resultados.total_procesados,
            venta=resultados.a_venta,
            reciclaje=resultados.a_reciclaje,
            desecho=resultados.a_desecho,
        )

        # 4) Mostrar metricas en el panel derecho (rentabilidad y espera
        #    quedan en 0 hasta implementar dinero y teoria de colas)
        self.panel_result.actualizar(
            total=resultados.total_procesados,
            espera_min=0,
            rentabilidad=0,
        )
