# ============================================================
#  resultados.py  -  Recoleccion de datos de salida
# ------------------------------------------------------------
#  AQUI VA: la estructura que acumula lo que pasa durante la
#  simulacion (cuantos a cada canal, tiempos de espera, costos)
#  y calcula las metricas finales que muestra el panel derecho.
#
#  NO va codigo visual ni el proceso SimPy. Solo guarda y calcula.
# ============================================================

from dataclasses import dataclass, field


@dataclass
class Resultados:
    """Acumula los datos generados durante una corrida."""

    total_procesados: int = 0
    a_venta: int = 0
    a_reciclaje: int = 0
    a_desecho: int = 0

    tiempos_espera: list = field(default_factory=list)  # espera de cada lote
    serie_arribos: list = field(default_factory=list)   # para grafico de arribos
    serie_ocupacion: list = field(default_factory=list) # para grafico de deposito

    rentabilidad: float = 0.0

    # ---- Calculos finales (se llaman al terminar la simulacion) ----
    def espera_promedio(self) -> float:
        if not self.tiempos_espera:
            return 0.0
        return sum(self.tiempos_espera) / len(self.tiempos_espera)

    def resumen(self) -> dict:
        """Devuelve las metricas listas para mostrar en el panel de resultados."""
        return {
            "total": self.total_procesados,
            "espera_min": round(self.espera_promedio()),
            "rentabilidad": self.rentabilidad,
        }
