# ============================================================
#  colas.py  -  Teoria de Colas (SimPy, M/M/c)
# ------------------------------------------------------------
#  AQUI VA: la simulacion de eventos discretos de la Mesa de
#  Clasificacion como un sistema de colas M/M/c:
#    - c servidores en paralelo  = cantidad_operarios
#    - servicio por dispositivo  = UNIF(1, 3) minutos
#    - disciplina FIFO
#
#  Reproduce la logica Seize -> Delay -> Release del DFD/Arena.
#  Mide los indicadores de Teoria de Colas:
#    Wq = tiempo medio de espera en cola
#    Lq = largo medio de la cola (via Little: Lq = Wq * lambda)
#    rho = utilizacion de los operarios
#
#  NO dibuja nada: devuelve un diccionario de metricas.
# ============================================================

import random
import simpy
from src.simulacion.parametros import Parametros
from src.simulacion.generadores import generar_lote, generar_cant_lotes


class MetricasColas:
    """Acumula las mediciones de la simulacion de colas."""
    def __init__(self):
        self.esperas = []          # tiempo en cola de cada dispositivo
        self.tiempo_ocupado = 0.0  # suma de tiempos de servicio (server-min)
        self.max_cola = 0          # largo maximo observado de la cola

    def wq(self) -> float:
        """Tiempo medio de espera en cola (minutos)."""
        return sum(self.esperas) / len(self.esperas) if self.esperas else 0.0

    def lq(self, duracion: float) -> float:
        """Largo medio de cola por Little: Lq = (suma de esperas) / tiempo total."""
        return sum(self.esperas) / duracion if duracion > 0 else 0.0

    def utilizacion(self, duracion: float, c: int) -> float:
        """Fraccion del tiempo que los operarios estuvieron ocupados (0 a 1)."""
        if duracion <= 0 or c <= 0:
            return 0.0
        return min(self.tiempo_ocupado / (duracion * c), 1.0)


def _atender(env, mesa, p, llegada, m: MetricasColas):
    """Proceso de UN dispositivo: pide operario, espera, es atendido."""
    # Registrar el largo de cola al llegar
    m.max_cola = max(m.max_cola, len(mesa.queue))
    with mesa.request() as turno:        # SEIZE
        yield turno
        m.esperas.append(env.now - llegada)
        dur = random.uniform(p.tiempo_servicio_min, p.tiempo_servicio_max)
        m.tiempo_ocupado += dur
        yield env.timeout(dur)           # DELAY (RELEASE al salir del with)


def _generar_llegadas(env, mesa, p, m: MetricasColas):
    """
    Genera los lotes a lo largo del periodo. Cada lote llega en un
    instante y vuelca todos sus dispositivos a la cola de la mesa.
    Los lotes se reparten uniformemente en el tiempo laborable.
    """
    total_min = p.minutos_periodo()

    # Armar la lista de lotes (todas las semanas) con su hora de arribo
    arribos = []
    for semana in range(p.semanas_simulacion):
        base = semana * p.dias_semana_laboral * p.horas_dia * 60
        ancho = p.dias_semana_laboral * p.horas_dia * 60
        for _ in range(generar_cant_lotes(p)):
            hora = base + random.uniform(0, ancho)
            arribos.append(hora)
    arribos.sort()

    # Disparar cada lote en su instante
    t_anterior = 0.0
    for hora in arribos:
        yield env.timeout(max(hora - t_anterior, 0))
        t_anterior = hora
        for d in generar_lote(p):
            env.process(_atender(env, mesa, p, env.now, m))


def simular_colas(p: Parametros) -> dict:
    """
    Corre la simulacion M/M/c de la mesa de clasificacion y
    devuelve las metricas de teoria de colas.
    """
    env = simpy.Environment()
    mesa = simpy.Resource(env, capacity=p.cantidad_operarios)
    m = MetricasColas()

    env.process(_generar_llegadas(env, mesa, p, m))
    env.run()   # corre hasta que no quedan eventos (todos atendidos)

    duracion = env.now
    # Ocupacion del deposito: cola maxima observada sobre la capacidad.
    # Puede superar el 100% (el deposito se desborda) -> dispara Alt. A.
    ocupacion = m.max_cola / p.capacidad_deposito if p.capacidad_deposito else 0.0
    return {
        "wq": m.wq(),                                        # min en cola
        "lq": m.lq(duracion),                                # dispositivos
        "utilizacion": m.utilizacion(duracion, p.cantidad_operarios),
        "max_cola": m.max_cola,
        "ocupacion": ocupacion,                              # 0 a 1+ (fraccion)
        "duracion": duracion,
        "atendidos": len(m.esperas),
    }
