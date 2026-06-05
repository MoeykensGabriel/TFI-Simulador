from dataclasses import dataclass
from src.simulacion import random_propio as random
from src.simulacion.parametros import Parametros


@dataclass
class Dispositivo:
    tipo: str
    moderno: bool
    peso: float
    canal: str = None
    mal_clasificado: bool = False


def generar_dispositivo(p: Parametros) -> Dispositivo:
    # distribucion binomial para tipo y moderno
    if random.random() <= p.prop_celular:
        tipo = "celular"
        peso = p.cel_peso_base + (p.cel_peso_rango * random.random())
    else:
        tipo = "tablet"
        peso = p.tab_peso_base + (p.tab_peso_rango * random.random())

    moderno = random.random() <= p.prop_moderno
    return Dispositivo(tipo=tipo, moderno=moderno, peso=round(peso, 3))


def generar_peso_lote(p: Parametros) -> float:
    # normal para peso del lote
    peso = random.gauss(p.tamano_lote_PROM, p.tamano_lote_DES)
    return max(peso, 1.0)


def generar_cant_lotes(p: Parametros) -> int:
    # uniforme para cantidad de lotes
    return int(p.lotes_semanales_A + (p.lotes_semanales_B * random.random()) )


def generar_lote(p: Parametros) -> list:
    # genera dispositivos hasta alcanzar el peso del lote
    peso_objetivo = generar_peso_lote(p)
    peso_acumulado = 0.0
    dispositivos = []

    while peso_acumulado <= peso_objetivo:
        d = generar_dispositivo(p)
        dispositivos.append(d)
        peso_acumulado += d.peso

    return dispositivos


def generar_lote_semana(p: Parametros) -> list:
    # genera semana completa con lotes aleatorios
    cantidad = generar_cant_lotes(p)
    return [generar_lote(p) for _ in range(cantidad)]
