# ============================================================
#  alternativas.py  -  Evaluacion de decisiones (A/B/C/D)
# ------------------------------------------------------------
#  AQUI VA: la logica condicional (IF/ELSE) de las 4 alternativas
#  del problema. Toma los resultados de la simulacion y decide,
#  para cada una, si la condicion se cumple y que recomendar.
#
#  Devuelve una lista de diccionarios lista para mostrar en la
#  ventana de recomendaciones. NO dibuja nada.
# ============================================================

from src.simulacion.parametros import Parametros
from src.simulacion.resultados import Resultados


def evaluar_alternativas(r: Resultados, p: Parametros) -> list:
    """Evalua las 4 alternativas y devuelve su diagnostico."""
    alternativas = []

    # ---- Alternativa A: Capacidad del Muelle ----
    # SI espera > 3 min Y ocupacion > 90% -> abrir 4a estacion
    cond_a = (r.wq_min > 3) and (r.ocupacion_deposito > 0.90)
    alternativas.append({
        "id": "A",
        "titulo": "Gestion de la Capacidad del Muelle",
        "condicion": "Espera > 3 min  Y  ocupacion deposito > 90%",
        "datos": f"Espera: {r.wq_min:.0f} min   |   Ocupacion: {r.ocupacion_deposito:.0%}",
        "activa": cond_a,
        "recomendacion": (
            "Autorizar la apertura de una 4a estacion de clasificacion temporal."
            if cond_a else
            "Mantener la operacion con 3 tecnicos para minimizar costos fijos."
        ),
    })

    # ---- Alternativa B: Transicion Tecnologica ----
    # SI % modernos > 35% (y cuello de botella en borrado) -> invertir
    cond_b = r.porcentaje_modernos > 0.35
    alternativas.append({
        "id": "B",
        "titulo": "Transicion Tecnologica",
        "condicion": "Dispositivos modernos > 35% del total",
        "datos": f"Modernos: {r.porcentaje_modernos:.0%}   ({r.modernos:,} de {r.total_procesados:,})".replace(",", "."),
        "activa": cond_b,
        "recomendacion": (
            "Invertir en la actualizacion de normas y software de tratamiento."
            if cond_b else
            "Mantener el protocolo actual, priorizando la rapidez del reciclaje basico."
        ),
    })

    # ---- Alternativa C: Precision de Clasificacion ----
    # SI perdida por error > margen de rentabilidad previsto (15% ingresos brutos)
    margen_previsto = p.margen_rentabilidad * r.ingresos_brutos
    cond_c = r.perdida_clasificacion > margen_previsto
    alternativas.append({
        "id": "C",
        "titulo": "Mejora en la Precision de Clasificacion",
        "condicion": f"Perdida por error > margen previsto ({p.margen_rentabilidad:.0%} de ingresos)",
        "datos": f"Perdida: $ {r.perdida_clasificacion:,.0f}   |   Margen: $ {margen_previsto:,.0f}".replace(",", "."),
        "activa": cond_c,
        "recomendacion": (
            "Implementar herramientas de diagnostico automatizado para los operarios."
            if cond_c else
            "Mantener el proceso manual, reforzando la capacitacion del personal."
        ),
    })

    # ---- Alternativa D: Puesto de Re-inspeccion ----
    # SI perdida acumulada por desecho erroneo > un salario tecnico
    cond_d = r.perdida_clasificacion > p.salario_tecnico
    alternativas.append({
        "id": "D",
        "titulo": "Activacion de Puesto de Re-inspeccion",
        "condicion": "Perdida por desecho erroneo > un salario tecnico",
        "datos": f"Perdida: $ {r.perdida_clasificacion:,.0f}   |   Salario: $ {p.salario_tecnico:,.0f}".replace(",", "."),
        "activa": cond_d,
        "recomendacion": (
            "Agregar un tecnico para re-inspeccionar la cola de desecho antes de inutilizar."
            if cond_d else
            "Confiar en el primer filtrado y concentrar al personal en el desmantelamiento."
        ),
    })

    return alternativas
