import simpy
from src.simulacion import random_propio as random
from src.simulacion.parametros import Parametros
from src.simulacion.generadores import generar_lote, generar_cant_lotes


class MetricasColas:
    def __init__(self):
        self.esperas = []
        self.tiempo_ocupado = 0.0
        self.max_cola = 0

    def wq(self) -> float:
        # tiempo medio de espera en cola
        return sum(self.esperas) / len(self.esperas) if self.esperas else 0.0

    def lq(self, duracion: float) -> float:
        # largo medio de cola por ley de little
        return sum(self.esperas) / duracion if duracion > 0 else 0.0

    def utilizacion(self, duracion: float, c: int) -> float:
        # rho = tiempo ocupado / (duracion * c operarios)
        if duracion <= 0 or c <= 0:
            return 0.0
        return min(self.tiempo_ocupado / (duracion * c), 1.0)

def _atender(env, mesa, p, llegada, m: MetricasColas):
    # seize, delay, release con uniforme para servicio
    m.max_cola = max(m.max_cola, len(mesa.queue))
    with mesa.request() as turno:
        yield turno
        m.esperas.append(env.now - llegada)
        dur = random.uniform(p.tiempo_servicio_min, p.tiempo_servicio_max)
        m.tiempo_ocupado += dur
        yield env.timeout(dur)


def _generar_llegadas(env, mesa, p, m: MetricasColas, duracion_semanas, lotes_semanas):
    # hora de arribo de cada lote (uniforme dentro de su semana)
    fin = p.minutos_periodo()
    arribos = []
    for semana in range(duracion_semanas):
        base = semana * p.dias_semana_laboral * p.horas_dia * 60
        ancho = p.dias_semana_laboral * p.horas_dia * 60
        for lote in lotes_semanas[semana]:
            arribos.append((base + random.uniform(0, ancho), lote))
    arribos.sort(key=lambda x: x[0])

    # los dispositivos de cada lote entran escalonados a la mesa,
    # repartidos entre el arribo del lote y el del lote siguiente
    eventos = []
    for i, (hora, lote) in enumerate(arribos):
        hora_sig = arribos[i + 1][0] if i + 1 < len(arribos) else fin
        ventana = max(hora_sig - hora, 1.0)
        n = len(lote) or 1
        for k in range(len(lote)):
            eventos.append(hora + ventana * (k / n))
    eventos.sort()

    t_anterior = 0.0
    for t in eventos:
        yield env.timeout(max(t - t_anterior, 0))
        t_anterior = t
        env.process(_atender(env, mesa, p, env.now, m))


def simular_colas(p: Parametros, duracion_semanas, lotes_semanas) -> dict:
    # simulacion de eventos discretos M/M/c
    env = simpy.Environment()
    mesa = simpy.Resource(env, capacity=p.cantidad_operarios)
    m = MetricasColas()

    env.process(_generar_llegadas(env, mesa, p, m, duracion_semanas, lotes_semanas))
    env.run()

    duracion = env.now
    ocupacion = m.max_cola / p.capacidad_deposito if p.capacidad_deposito else 0.0
    return {
        "wq": m.wq(),
        "lq": m.lq(duracion),
        "utilizacion": m.utilizacion(duracion, p.cantidad_operarios),
        "max_cola": m.max_cola,
        "ocupacion": ocupacion,
        "duracion": duracion,
        "atendidos": len(m.esperas),
    }
