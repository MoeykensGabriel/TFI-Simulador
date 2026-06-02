# ============================================================
#  resultados.py  -  Recoleccion de datos de salida
# ------------------------------------------------------------
#  AQUI VA: la estructura que acumula lo que pasa durante la
#  simulacion (cuantos a cada canal, dinero, errores, tiempos)
#  y calcula las metricas finales que muestra el panel derecho.
#
#  NO va codigo visual ni el proceso SimPy. Solo guarda y calcula.
# ============================================================

from dataclasses import dataclass, field


@dataclass
class Resultados:
    """Acumula los datos generados durante una corrida."""

    # --- Conteos por canal ---
    total_procesados: int = 0
    total_lotes: int = 0          # cantidad de lotes recibidos en el periodo
    a_venta: int = 0
    a_reciclaje: int = 0
    a_desecho: int = 0
    mal_clasificados: int = 0     # reventa que terminaron en desecho
    modernos: int = 0             # dispositivos de tecnologia moderna

    # --- Dinero (ARS) ---
    ganancia_reventa: float = 0.0     # GTR: por dispositivos vendidos
    ganancia_materiales: float = 0.0  # GTM: por materiales reciclados
    perdida_clasificacion: float = 0.0  # valor de reventa perdido por error
    costo_operativo: float = 0.0      # salarios de los operarios

    # --- Teoria de colas (mesa M/M/c) ---
    wq_min: float = 0.0           # tiempo medio de espera en cola (min)
    lq: float = 0.0               # largo medio de la cola (dispositivos)
    utilizacion: float = 0.0      # utilizacion de operarios (0 a 1)
    max_cola: int = 0             # cola maxima observada
    ocupacion_deposito: float = 0.0  # fraccion ocupada del deposito (0 a 1+)

    # --- Series para graficos ---
    serie_arribos: list = field(default_factory=list)
    serie_ocupacion: list = field(default_factory=list)
    tiempos_espera: list = field(default_factory=list)

    # ---- Calculos finales ----
    @property
    def ganancia_neta(self) -> float:
        """GTN = ingresos (reventa + materiales) - costo operativo."""
        return self.ganancia_reventa + self.ganancia_materiales - self.costo_operativo

    @property
    def promedio_por_lote(self) -> float:
        """Dispositivos promedio por lote recibido."""
        if self.total_lotes == 0:
            return 0.0
        return self.total_procesados / self.total_lotes

    @property
    def porcentaje_modernos(self) -> float:
        """Fraccion de dispositivos modernos (0 a 1)."""
        if self.total_procesados == 0:
            return 0.0
        return self.modernos / self.total_procesados

    @property
    def ingresos_brutos(self) -> float:
        """Ingresos antes de costos (reventa + materiales)."""
        return self.ganancia_reventa + self.ganancia_materiales

    def espera_promedio(self) -> float:
        if not self.tiempos_espera:
            return 0.0
        return sum(self.tiempos_espera) / len(self.tiempos_espera)

    def resumen(self) -> dict:
        """Metricas listas para mostrar en el panel de resultados."""
        return {
            "total": self.total_procesados,
            "espera_min": round(self.espera_promedio()),
            "rentabilidad": self.ganancia_neta,
        }
