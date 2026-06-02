# ============================================================
#  modelo.py  -  Motor de simulacion
# ------------------------------------------------------------
#  AQUI VA: la orquestacion de una corrida completa. Por ahora
#  ejecuta el "modelo matematico" (conteo del DFD):
#    genera semanas -> desagrega lotes -> clasifica dispositivos
#    -> acumula los totales en Resultados.
#
#  Se puede correr completo (correr) o avanzar semana a semana
#  (correr_semana), que es lo que usa la GUI para animar.
#
#  La parte de Teoria de Colas (SimPy: tiempos de espera,
#  utilizacion) se agrega en un paso posterior.
# ============================================================

from src.simulacion.parametros import Parametros
from src.simulacion.resultados import Resultados
from src.simulacion.generadores import generar_semana
from src.simulacion.clasificador import clasificar
from src.simulacion.calculadora import valor_reventa, valor_materiales, costo_operarios


class ModeloSimulacion:
    def __init__(self, parametros: Parametros):
        self.p = parametros
        self.resultados = Resultados()

    def correr_semana(self) -> Resultados:
        """
        Procesa UNA semana: genera sus lotes, desagrega y clasifica
        cada dispositivo, y acumula los totales en self.resultados.
        Devuelve los resultados parciales (acumulados hasta ahora).
        """
        r = self.resultados
        semana = generar_semana(self.p)
        for lote in semana:
            for d in lote:
                clasificar(d, self.p)
                r.total_procesados += 1

                if d.canal == "reventa":
                    r.a_venta += 1
                    r.ganancia_reventa += valor_reventa(d, self.p)
                elif d.canal == "reciclaje":
                    r.a_reciclaje += 1
                    r.ganancia_materiales += valor_materiales(d, self.p)
                else:  # desecho
                    r.a_desecho += 1
                    if d.mal_clasificado:
                        # era reventa: se perdio el valor que habria tenido
                        r.mal_clasificados += 1
                        r.perdida_clasificacion += valor_reventa(d, self.p)

        # El costo operativo es fijo del periodo (no por semana):
        # se recalcula con el total de operarios cada vez.
        r.costo_operativo = costo_operarios(self.p)
        return r

    def correr(self) -> Resultados:
        """Corre la simulacion completa (todas las semanas de una)."""
        for _ in range(self.p.semanas_simulacion):
            self.correr_semana()
        return self.resultados
