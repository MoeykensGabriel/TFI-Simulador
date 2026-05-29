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
    lotes_semanales_A: float = 3.0        # Cantidad mínima de lotes que llegan por semana
    lotes_semanales_B: float = 7.0        # Cantidad máxima de lotes que llegan por semana

    tamano_lote_PROM: int = 9000           # unidades por lote
    tamano_lote_DES: int = 200           # unidades por lote

    # --- Clasificacion ---
    cantidad_operarios: int = 3      # operarios en la mesa de clasificacion
    error_clasificacion: float = 3.0 # % de error de clasificacion manual

    # --- Proporciones de salida (se ajustaran con datos reales) ---
    # Que % de cada lote va a cada canal
    prop_venta: float = 0.37
    prop_reciclaje: float = 0.46
    prop_desecho: float = 0.17

    # --- Duracion de la simulacion ---
    semanas_simulacion: int = 4

    @classmethod
    def desde_gui(cls, valores: dict) -> "Parametros":
        """Crea un Parametros a partir del diccionario que entrega la GUI."""
        return cls(
            lotes_semanales_A=valores["lotes_A"],
            lotes_semanales_B=valores["lotes_B"],
            tamano_lote_PROM=valores["lote_PROM"],
            tamano_lote_DES=valores["lote_DES"],
            cantidad_operarios=valores["operarios"],
            error_clasificacion=valores["error"],
            semanas_simulacion=valores["semanas"],
        )
