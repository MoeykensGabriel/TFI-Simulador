# ============================================================
#  modelo.py  -  Motor de simulacion
# ------------------------------------------------------------
#  AQUI VA: la orquestacion de una corrida completa. Por ahora
#  ejecuta el "modelo matematico" (conteo del DFD):
#    genera semanas -> desagrega lotes -> clasifica dispositivos
#    -> acumula los totales en Resultados.
#
#  La parte de Teoria de Colas (SimPy: tiempos de espera,
#  utilizacion) se agrega en un paso posterior.
# ============================================================

from src.simulacion.parametros import Parametros
from src.simulacion.resultados import Resultados
from src.simulacion.generadores import generar_semana
from src.simulacion.clasificador import clasificar


class ModeloSimulacion:
    def __init__(self, parametros: Parametros):
        self.p = parametros
        self.resultados = Resultados()

    def correr(self) -> Resultados:
        """
        Corre la simulacion completa (semana a semana) y devuelve
        los resultados con los conteos por canal.
        """
        r = self.resultados

        for _ in range(self.p.semanas_simulacion):
            semana = generar_semana(self.p)          # lista de lotes
            for lote in semana:
                for d in lote:
                    clasificar(d, self.p)            # asigna canal
                    r.total_procesados += 1
                    if d.canal == "reventa":
                        r.a_venta += 1
                    elif d.canal == "reciclaje":
                        r.a_reciclaje += 1
                    else:
                        r.a_desecho += 1

        return r
