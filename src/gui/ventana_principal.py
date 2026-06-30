# ventana_principal.py - ventana raiz: arma header + 3 paneles y orquesta todo

import tkinter as tk
from src.gui.tema import COLORES, FUENTES, MEDIDAS, aplicar_estilo_ttk, aplicar_tema
from src.gui.panel_parametros import PanelParametros
from src.gui.panel_flujo import PanelFlujo
from src.gui.panel_resultados import PanelResultados
from src.gui.ventana_recomendaciones import VentanaRecomendaciones
from src.simulacion.parametros import Parametros
from src.simulacion.modelo import ModeloSimulacion
from src.simulacion.alternativas import evaluar_alternativas


class VentanaPrincipal:
    PAUSA_SEMANA = 3000
    PAUSA_PUNTOS = 400

    def __init__(self, root: tk.Tk):
        self.root = root
        self.simulando = False
        self.modo = "claro"
        self._run_id = 0
        self.ultimo_r = None
        self.serie = []
        self._configurar_ventana()
        self._construir_ui()

    def _configurar_ventana(self):
        self.root.title("Simulador de Clasificacion de RAEE | Scrap y Rezagos S.R.L.")
        ancho, alto = MEDIDAS["ancho_ventana"], MEDIDAS["alto_ventana"]
        aplicar_estilo_ttk(self.root)
        self.root.update_idletasks()
        x = (self.root.winfo_screenwidth()  - ancho) // 2
        y = (self.root.winfo_screenheight() - alto)  // 2
        self.root.geometry(f"{ancho}x{alto}+{x}+{y}")
        self.root.minsize(1100, 640)

    # ----------------------------------------------------------
    #  Construccion de la UI (se rehace al cambiar de tema)
    # ----------------------------------------------------------
    def _construir_ui(self):
        self.root.configure(bg=COLORES["fondo"])
        self._header()
        self._cuerpo()

    def _header(self):
        barra = tk.Frame(self.root, bg=COLORES["header"], height=82)
        barra.pack(fill="x")
        barra.pack_propagate(False)

        izq = tk.Frame(barra, bg=COLORES["header"])
        izq.pack(side="left", padx=22)
        tk.Label(izq, text="Simulador de Clasificacion de RAEE",
        bg=COLORES["header"], fg=COLORES["texto_claro"],
        font=FUENTES["titulo_app"], anchor="w").pack(anchor="w", pady=(14, 0))
        tk.Label(izq, text="Optimizacion del proceso de clasificacion  -  v1.0",
        bg=COLORES["header"], fg=COLORES["subtexto"],
        font=FUENTES["subtitulo_app"], anchor="w").pack(anchor="w", pady=(2, 0))

        tk.Label(barra, text="Scrap & Rezagos S.R.L.",
        bg=COLORES["header"], fg=COLORES["header_acento"],
        font=FUENTES["valor_medio"]).pack(side="right", padx=22)

        # boton de modo oscuro / claro
        texto = "🌙  Modo oscuro" if self.modo == "claro" else "☀  Modo claro"
        btn = tk.Button(barra, text=texto, bg=COLORES["acento"], fg="white",
                        font=FUENTES["texto_normal"], relief="flat", bd=0,
                        padx=12, pady=6, cursor="hand2",
                        activebackground=COLORES["boton_hover"], activeforeground="white",
                        command=self._toggle_tema)
        btn.pack(side="right", padx=(0, 8))

        tk.Frame(self.root, bg=COLORES["header_acento"], height=3).pack(fill="x")

    def _cuerpo(self):
        cuerpo = tk.Frame(self.root, bg=COLORES["fondo"])
        cuerpo.pack(fill="both", expand=True, padx=10, pady=10)

        self.panel_param = PanelParametros(cuerpo, al_iniciar=self._ejecutar_simulacion)
        self.panel_param.pack(side="left", fill="y")
        self.panel_param.configure(width=MEDIDAS["ancho_param"])
        self.panel_param.pack_propagate(False)

        self.panel_flujo = PanelFlujo(cuerpo)
        self.panel_flujo.pack(side="left", fill="both", expand=True, padx=10)

        self.panel_result = PanelResultados(cuerpo, al_ver_recomendaciones=self._abrir_recomendaciones)
        self.panel_result.pack(side="left", fill="y")
        self.panel_result.configure(width=MEDIDAS["ancho_result"])
        self.panel_result.pack_propagate(False)

    def _toggle_tema(self):
        """Cambia claro/oscuro: detiene la corrida, recolorea y reconstruye la UI."""
        self.simulando = False
        self._run_id += 1   # invalida cualquier loop de simulacion en curso
        self.modo = "oscuro" if self.modo == "claro" else "claro"
        estado_params = None
        if hasattr(self, "panel_param"):
            estado_params = self.panel_param.estado()

        aplicar_tema(self.modo)
        aplicar_estilo_ttk(self.root)
        for w in self.root.winfo_children():
            w.destroy()
        self._construir_ui()

        if estado_params:
            self.panel_param.restaurar(estado_params)
        self._restaurar_resultados()

    def _restaurar_resultados(self):
        """Tras reconstruir la UI, vuelve a mostrar los resultados de la ultima corrida."""
        r = self.ultimo_r
        if r is None:
            return
        self.panel_flujo.actualizar(entrada=r.total_procesados, clasificados=r.total_procesados,
                                    venta=r.a_venta, reciclaje=r.a_reciclaje, desecho=r.a_desecho)
        self.panel_flujo.actualizar_progreso(self.total_semanas, self.total_semanas)
        self.panel_flujo.actualizar_deposito(r.ocupacion_deposito)
        self.panel_flujo.actualizar_estado(
            f"Simulacion finalizada ({self.total_semanas} semanas)", color=COLORES["ok"])
        self.panel_result.actualizar(total=r.total_procesados, espera_min=round(r.wq_min),
                                     rentabilidad=r.ganancia_neta, promedio_lote=r.promedio_por_lote)
        self.panel_result.mostrar_graficos(self.serie)
        self.panel_result.mostrar_boton_recomendaciones()

    # ----------------------------------------------------------
    #  Conexion GUI <-> simulacion
    # ----------------------------------------------------------
    def _ejecutar_simulacion(self, valores):
        """Arranca/detiene la simulacion semana a semana."""
        if self.simulando:
            self.simulando = False
            self.total_semanas = self.semana_actual
            return False
        p = Parametros.desde_gui(valores)
        self.modelo = ModeloSimulacion(p)
        self.total_semanas = p.semanas_simulacion
        self.lotes_semanas = []
        self.serie = []
        self._prev_procesados = 0
        self.ultimo_r = None
        self.semana_actual = 1
        self.simulando = True
        self._run_id += 1
        rid = self._run_id
        self._puntos = 0
        self.panel_result.esconder_boton_recomendaciones()
        self.panel_result.mostrar_graficos([])   # resetea a graficos vacios
        self.panel_flujo.actualizar_deposito(0)
        self.panel_flujo.actualizar_progreso(0, self.total_semanas)
        self.panel_flujo.limpiar_animacion()
        self._animar_puntos(rid)
        self._procesar_semana(rid)
        return True

    def _animar_puntos(self, rid):
        """Hace parpadear los puntos del aviso (. .. ...) mientras simula."""
        if not self.simulando or rid != self._run_id:
            return
        self._puntos = (self._puntos + 1) % 4
        texto = f"Simulando semana {self.semana_actual} de {self.total_semanas}"
        self.panel_flujo.actualizar_estado(texto + "." * self._puntos, color=COLORES["acento"])
        self.root.after(self.PAUSA_PUNTOS, lambda: self._animar_puntos(rid))

    def _procesar_semana(self, rid):
        """Procesa una semana, actualiza los paneles y agenda la siguiente."""
        if rid != self._run_id:
            return
        r = self.modelo.correr_semana()
        self.lotes_semanas.append(r.lotes_semana)
        self.panel_flujo.actualizar_progreso(self.semana_actual, self.total_semanas)

        # serie semanal para los graficos
        arribos = r.total_procesados - self._prev_procesados
        self._prev_procesados = r.total_procesados
        self.serie.append({"semana": self.semana_actual, "arribos": arribos,
                           "neta": r.ganancia_neta})

        self.panel_flujo.actualizar(entrada=r.total_procesados, clasificados=r.total_procesados,
                                    venta=r.a_venta, reciclaje=r.a_reciclaje, desecho=r.a_desecho)
        self.panel_flujo.animar_semana((r.a_venta, r.a_reciclaje, r.a_desecho))
        self.panel_result.actualizar(total=r.total_procesados, espera_min=round(r.wq_min),
                                     rentabilidad=r.ganancia_neta, promedio_lote=r.promedio_por_lote)

        if not self.simulando or self.semana_actual >= self.total_semanas:
            self._finalizar(r)
            return

        def siguiente():
            if rid != self._run_id:
                return
            if not self.simulando:
                self._finalizar(r)
                return
            self.semana_actual += 1
            self._procesar_semana(rid)

        self.root.after(self.PAUSA_SEMANA, siguiente)

    def _finalizar(self, r):
        """Cierra la simulacion: corre las colas, muestra metricas, graficos y el boton."""
        self.simulando = False
        self.modelo.calcular_colas(self.total_semanas, self.lotes_semanas)
        self.ultimo_r = r
        self.panel_result.actualizar(total=r.total_procesados, espera_min=round(r.wq_min),
                                     rentabilidad=r.ganancia_neta, promedio_lote=r.promedio_por_lote)
        self.panel_result.mostrar_graficos(self.serie)
        self.panel_flujo.actualizar_deposito(r.ocupacion_deposito)
        self.panel_flujo.actualizar_estado(
            f"Simulacion finalizada ({self.semana_actual} semanas)", color=COLORES["ok"])
        self.alternativas = evaluar_alternativas(r, self.modelo.p)
        self.panel_result.mostrar_boton_recomendaciones()
        self.panel_param.resetear_boton()

    def _abrir_recomendaciones(self):
        if hasattr(self, "alternativas"):
            VentanaRecomendaciones(self.root, self.alternativas)
