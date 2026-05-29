# ============================================================
#  modelo.py  -  Motor de simulacion (SimPy)
# ------------------------------------------------------------
#  AQUI VA: el corazon del simulador. Define los procesos de
#  eventos discretos con SimPy:
#    - llegada de lotes (segun el TEA y distribuciones de prob.)
#    - cola hacia la mesa de clasificacion (recurso = operarios)
#    - clasificacion y derivacion a cada canal (con su % de error)
#
#  Lee un objeto Parametros y va llenando un objeto Resultados.
#  NO contiene nada visual.
#
#  ESTADO: esqueleto. La logica completa se desarrolla en el
#  proximo avance, paso a paso.
# ============================================================

import simpy
from src.simulacion.parametros import Parametros
from src.simulacion.resultados import Resultados


class ModeloSimulacion:
    def __init__(self, parametros: Parametros):
        self.p = parametros
        self.resultados = Resultados()
        self.env = simpy.Environment()
        # La mesa de clasificacion como recurso limitado por la
        # cantidad de operarios disponibles.
        self.mesa = simpy.Resource(self.env, capacity=self.p.cantidad_operarios)

    # --- Procesos SimPy (a desarrollar) ---
    def _generar_lotes(self):
        """Genera lotes que llegan al muelle segun el TEA. (pendiente)"""
        raise NotImplementedError

    def _clasificar(self, lote):
        """Procesa un lote en la mesa y lo deriva a un canal. (pendiente)"""
        raise NotImplementedError

    # --- Ejecucion ---
    def correr(self) -> Resultados:
        """Corre la simulacion completa y devuelve los resultados."""
        # self.env.process(self._generar_lotes())
        # self.env.run(until=self.p.horas_simulacion)
        return self.resultados
