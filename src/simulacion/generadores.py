# ============================================================
#  generadores.py  -  Generacion aleatoria (DFD)
# ------------------------------------------------------------
#  AQUI VA: las funciones que generan los elementos aleatorios
#  del modelo, siguiendo el DFD:
#    - generar_dispositivo : tipo + moderno? + peso
#    - generar_peso_lote   : Normal(450, 100)
#    - generar_cant_lotes  : 3 + 4u  (entre lotes_min y lotes_max)
#
#  Reciben un objeto Parametros y devuelven valores concretos.
#  NO usan SimPy ni dibujan nada: solo numeros.
# ============================================================

from dataclasses import dataclass
from src.simulacion import random_propio as random
from src.simulacion.parametros import Parametros


@dataclass
class Dispositivo:
    """Un dispositivo individual generado al desagregar un lote."""
    tipo: str        # "celular" o "tablet"
    moderno: bool    # True si es de tecnologia moderna
    peso: float      # kg

    # Se completan en la etapa de clasificacion:
    canal: str = None          # "reventa" | "reciclaje" | "desecho"
    mal_clasificado: bool = False  # True si era reventa y fue a desecho por error


def generar_dispositivo(p: Parametros) -> Dispositivo:
    """
    Genera UN dispositivo segun el DFD:
    u <= prop_celular -> celular (peso 0.14 + 0.16u)
    u >  prop_celular -> tablet  (peso 0.30 + 0.40u)
    Luego decide si es moderno (prop_moderno) y calcula su peso.
    """
    # 1) Tipo de dispositivo
    if random.random() <= p.prop_celular:
        tipo = "celular"
        peso = p.cel_peso_base + (p.cel_peso_rango * random.random())
    else:
        tipo = "tablet"
        peso = p.tab_peso_base + (p.tab_peso_rango * random.random())

    # 2) Es moderno?
    moderno = random.random() <= p.prop_moderno

    return Dispositivo(tipo=tipo, moderno=moderno, peso=round(peso, 3))


def generar_peso_lote(p: Parametros) -> float:
    """Peso del lote en kg ~ Normal(media, desviacion). Nunca negativo."""
    peso = random.gauss(p.tamano_lote_PROM, p.tamano_lote_DES)
    return max(peso, 1.0)


def generar_cant_lotes(p: Parametros) -> int:
    """Cantidad de lotes de la semana, entero entre lotes_min y lotes_max."""
    return int(p.lotes_semanales_A + (p.lotes_semanales_B * random.random()) )


def generar_lote(p: Parametros) -> list:
    """
    Genera UN lote completo (loop SP <= PL del DFD):
    1. Sortea el peso del lote PL ~ Normal(450, 100).
    2. Va generando dispositivos y acumulando su peso SP
    hasta que SP alcanza PL.
    Devuelve la lista de Dispositivos que componen el lote.
    """
    peso_objetivo = generar_peso_lote(p)   # PL
    peso_acumulado = 0.0                   # SP
    dispositivos = []

    while peso_acumulado <= peso_objetivo:
        d = generar_dispositivo(p)# Solo para debug
        dispositivos.append(d)
        peso_acumulado += d.peso            # SP = SP + PD

    return dispositivos


def generar_lote_semana(p: Parametros) -> list:
    """
    Genera una semana completa: L lotes (entre min y max), cada uno
    desagregado en dispositivos. Devuelve la lista de lotes,
    donde cada lote es una lista de Dispositivos.
    """
    cantidad = generar_cant_lotes(p)        # L
    return [generar_lote(p) for _ in range(cantidad)]
