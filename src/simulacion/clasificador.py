# ============================================================
#  clasificador.py  -  Etapa de clasificacion (DFD)
# ------------------------------------------------------------
#  AQUI VA: la logica que decide a que canal va cada dispositivo
#  (Reventa / Reciclaje / Desecho) segun las probabilidades del
#  documento, y aplica el 3% de error de clasificacion manual
#  (equipos de reventa que terminan en desecho -> mal clasificados).
#
#  Reproduce los bloques CLASIFICACION DISPOSITIVO del DFD.
#  NO usa SimPy ni dibuja: solo decide el canal.
# ============================================================

from src.simulacion import random_propio as random
from src.simulacion.parametros import Parametros
from src.simulacion.generadores import Dispositivo


def clasificar(d: Dispositivo, p: Parametros) -> Dispositivo:
    """
    Asigna un canal al dispositivo usando una variable uniforme U(0,1)
    contra las probabilidades acumuladas:
        u <= 0.37          -> Reventa
        u <= 0.83          -> Reciclaje
        resto              -> Desecho

    Luego aplica el error del 3%: si cayo en Reventa, con probabilidad
    'error_clasificacion' se desvia a Desecho y se marca mal_clasificado.
    """
    u = random.random()

    if u <= p.prop_venta:
        canal = "reventa"
    elif u <= p.prop_venta + p.prop_reciclaje:
        canal = "reciclaje"
    else:
        canal = "desecho"

    # Error de clasificacion: reventa -> desecho (CMC / TMC del diccionario)
    mal_clasificado = False
    if canal == "reventa" and random.random() <= p.error_clasificacion:
        canal = "desecho"
        mal_clasificado = True

    d.canal = canal
    d.mal_clasificado = mal_clasificado
    return d
