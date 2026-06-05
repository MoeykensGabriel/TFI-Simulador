
from src.simulacion import random_propio as random
from src.simulacion.parametros import Parametros
from src.simulacion.generadores import Dispositivo


def clasificar(d: Dispositivo, p: Parametros) -> Dispositivo:
    # distribucion binomial para canal y error 3%
    u = random.random()

    if u <= p.prop_venta:
        canal = "reventa"
    elif u <= p.prop_venta + p.prop_reciclaje:
        canal = "reciclaje"
    else:
        canal = "desecho"

    mal_clasificado = False
    if canal == "reventa" and random.random() <= p.error_clasificacion:
        canal = "desecho"
        mal_clasificado = True

    d.canal = canal
    d.mal_clasificado = mal_clasificado
    return d
