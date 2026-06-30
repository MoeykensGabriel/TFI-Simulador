
from src.simulacion import random_propio as random
from src.simulacion.parametros import Parametros
from src.simulacion.generadores import Dispositivo


def valor_reventa(d: Dispositivo, p: Parametros) -> float:
    # uniforme para precio de reventa segun tipo
    if d.tipo == "celular":
        return random.uniform(p.cel_precio_min, p.cel_precio_max)
    else:
        return random.uniform(p.tab_precio_min, p.tab_precio_max)


def valor_materiales(d: Dispositivo, p: Parametros) -> float:
    # composicion porcentual de materiales
    plastico = d.peso * p.recic_plastico_prop * p.recic_plastico_precio
    metal    = d.peso * p.recic_metal_prop    * p.recic_metal_precio
    resto    = d.peso * p.recic_resto_prop    * p.recic_resto_precio
    return plastico + metal + resto


def costo_operarios(p: Parametros) -> float:
    # salario mensual escalado por la duracion simulada (4 semanas = 1 mes)
    meses = p.semanas_simulacion / 4.0
    return p.cantidad_operarios * p.salario_tecnico * meses
