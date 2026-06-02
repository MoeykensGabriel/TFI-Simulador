# ============================================================
#  calculadora.py  -  Calculo economico (DFD)
# ------------------------------------------------------------
#  AQUI VA: el dinero que genera (o pierde) cada dispositivo
#  segun su canal, reproduciendo los bloques PRECIO REVENTA y
#  CALCULO MATERIALES del DFD.
#
#  - reventa     -> precio de venta (uniforme segun tipo)
#  - reciclaje   -> valor de materiales (plastico + metal)
#  - mal clasif. -> perdida = el precio de reventa que se perdio
#
#  NO usa SimPy ni dibuja: solo devuelve numeros.
# ============================================================

from src.simulacion import random_propio as random
from src.simulacion.parametros import Parametros
from src.simulacion.generadores import Dispositivo


def valor_reventa(d: Dispositivo, p: Parametros) -> float:
    """
    Precio de reventa de UN dispositivo, uniforme segun su tipo:
      celular: U(cel_precio_min, cel_precio_max)
      tablet:  U(tab_precio_min, tab_precio_max)
    """
    if d.tipo == "celular":
        return random.uniform(p.cel_precio_min, p.cel_precio_max)
    else:
        return random.uniform(p.tab_precio_min, p.tab_precio_max)


def valor_materiales(d: Dispositivo, p: Parametros) -> float:
    """
    Valor de los materiales recuperados al reciclar UN dispositivo.
    El peso se reparte en plastico / metal / resto y se valoriza:
      plastico = peso * 0.40 * $1.450/kg
      metal    = peso * 0.35 * $45.100/kg
      resto    = peso * 0.25 * $0/kg
    """
    plastico = d.peso * p.recic_plastico_prop * p.recic_plastico_precio
    metal    = d.peso * p.recic_metal_prop    * p.recic_metal_precio
    resto    = d.peso * p.recic_resto_prop    * p.recic_resto_precio
    return plastico + metal + resto


def costo_operarios(p: Parametros) -> float:
    """Costo fijo del periodo: un salario por operario."""
    return p.cantidad_operarios * p.salario_tecnico
