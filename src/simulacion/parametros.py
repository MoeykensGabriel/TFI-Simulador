# ============================================================
#  parametros.py  -  Variables de entrada del modelo
# ------------------------------------------------------------
#  AQUI VA: TODAS las variables configurables de la simulacion,
#  en un solo lugar. El panel de parametros (GUI) llena estos
#  valores y el modelo SimPy los lee.
#
#  NO va logica de simulacion ni codigo visual. Solo datos.
# ============================================================

from dataclasses import dataclass


@dataclass
class Parametros:
    """Contenedor de todos los parametros de una corrida de simulacion."""

    # --- Entrada de lotes ---
    tea_promedio: float = 6.0        # Tiempo Entre Arribos promedio (horas)
    tamano_lote: int = 200           # unidades por lote

    # --- Clasificacion ---
    cantidad_operarios: int = 5      # operarios en la mesa de clasificacion
    error_clasificacion: float = 3.0 # % de error de clasificacion manual

    # --- Proporciones de salida (se ajustaran con datos reales) ---
    # Que % de cada lote va a cada canal
    prop_venta: float = 0.20
    prop_reciclaje: float = 0.35
    prop_desecho: float = 0.45

    # --- Duracion de la simulacion ---
    horas_simulacion: int = 720      # 720 h = 1 mes aprox.

    @classmethod
    def desde_gui(cls, valores: dict) -> "Parametros":
        """Crea un Parametros a partir del diccionario que entrega la GUI."""
        return cls(
            tea_promedio=valores["tea"],
            tamano_lote=valores["lote"],
            cantidad_operarios=valores["operarios"],
            error_clasificacion=valores["error"],
        )
