# ============================================================
#  parametros.py  -  Variables de entrada del modelo
# ------------------------------------------------------------
#  AQUI VA: TODAS las variables configurables de la simulacion,
#  en un solo lugar. El panel de parametros (GUI) llena estos
#  valores y el modelo SimPy los lee.
#
#  NO va logica de simulacion ni codigo visual. Solo datos.
#  Valores tomados del documento de Scrap y Rezagos S.R.L.
# ============================================================

from dataclasses import dataclass


@dataclass
class Parametros:
    """Contenedor de todos los parametros de una corrida de simulacion."""

    # --- Entrada de lotes ---
    lotes_semanales_A: float = 3.0    # cantidad MINIMA de lotes por semana
    lotes_semanales_B: float = 7.0    # cantidad MAXIMA de lotes por semana

    tamano_lote_PROM: float = 450.0   # kg, media del peso del lote (Normal)
    tamano_lote_DES: float = 100.0    # kg, desviacion del peso del lote (Normal)

    # --- Composicion del lote ---
    prop_celular: float = 0.97        # 97% celulares
    prop_tablet: float = 0.03         # 3% tablets
    prop_moderno: float = 0.30        # 30% de tecnologia moderna

    # --- Pesos por dispositivo (kg) -> PD = base + rango * U(0,1) ---
    cel_peso_base: float = 0.14       # celular: 140-300 g  -> 0.14 + 0.16u
    cel_peso_rango: float = 0.16
    tab_peso_base: float = 0.30       # tablet:  300-700 g  -> 0.30 + 0.40u
    tab_peso_rango: float = 0.40

    # --- Clasificacion ---
    cantidad_operarios: int = 3       # operarios en la mesa de clasificacion
    error_clasificacion: float = 0.03 # 3% de error (reventa -> desecho)

    # --- Teoria de colas (mesa de clasificacion M/M/c) ---
    tiempo_servicio_min: float = 1.0  # min, servicio por dispositivo UNIF(1,3)
    tiempo_servicio_max: float = 3.0
    horas_dia: int = 8                # jornada: horas por dia
    dias_semana_laboral: int = 5      # jornada: dias por semana
    capacidad_deposito: int = 10000   # capacidad del deposito (dispositivos)

    # --- Probabilidades de canal (acumuladas: 0.30 / 0.70 / 1.00) ---
    prop_venta: float = 0.30
    prop_reciclaje: float = 0.40
    prop_desecho: float = 0.30

    # --- Precios de reventa (ARS por unidad) ---
    cel_precio_min: float = 150_000
    cel_precio_max: float = 350_000
    tab_precio_min: float = 250_000
    tab_precio_max: float = 550_000

    # --- Reciclaje: composicion de materiales y precio (ARS por kg) ---
    recic_plastico_prop: float = 0.40
    recic_plastico_precio: float = 1_450
    recic_metal_prop: float = 0.35
    recic_metal_precio: float = 45_100
    recic_resto_prop: float = 0.25
    recic_resto_precio: float = 0

    # --- Economia / decisiones ---
    margen_rentabilidad: float = 0.15  # 15% sobre ingresos brutos
    salario_tecnico: float = 1_100_000 # ARS por operario/mes

    # --- Duracion de la simulacion ---
    semanas_simulacion: int = 4        # 4 a 12 semanas

    def minutos_periodo(self) -> float:
        """Minutos laborables totales del periodo simulado."""
        return self.semanas_simulacion * self.dias_semana_laboral * self.horas_dia * 60

    @classmethod
    def desde_gui(cls, valores: dict) -> "Parametros":
        """Crea un Parametros a partir del diccionario que entrega la GUI."""
        return cls(
            lotes_semanales_A=valores["lotes_min"],
            lotes_semanales_B=valores["lotes_max"],
            tamano_lote_PROM=valores["lote_media"],
            tamano_lote_DES=valores["lote_desv"],
            cel_precio_min=valores["cel_precio_min"],
            cel_precio_max=valores["cel_precio_max"],
            tab_precio_min=valores["tab_precio_min"],
            tab_precio_max=valores["tab_precio_max"],
            prop_venta=valores.get("prop_venta", 0.30),
            prop_reciclaje=valores.get("prop_reciclaje", 0.40),
            prop_desecho=valores.get("prop_desecho", 0.30),
            margen_rentabilidad=valores["margen"] / 100,
            cantidad_operarios=valores["operarios"],
            salario_tecnico=valores["salario"],
            semanas_simulacion=valores["semanas"],
        )
