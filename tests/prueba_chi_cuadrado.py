import sys
import os

# prueba chi cuadrado para validar uniformidad del generador congruencial
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.simulacion import random_propio as random

# tabla chi cuadrado a 5% de significancia
CHI2_TABLA_005 = {
    4: 9.488,
    5: 11.070,
    9: 16.919,
    14: 23.685,
    19: 30.144,
    49: 66.339,
}


def prueba_uniformidad(n=10000, k=10, semilla=12345, alfa=0.05):
    # chi2 = suma((observado - esperado)^2 / esperado)
    random.semilla(semilla)

    observadas = [0] * k
    for _ in range(n):
        u = random.random()
        clase = int(u * k)
        if clase == k:
            clase = k - 1
        observadas[clase] += 1

    esperada = n / k

    chi2 = 0.0
    print(f"\n  Clase        Intervalo        O_i        E_i      (O-E)^2/E")
    print("  " + "-" * 56)
    for i in range(k):
        inf = i / k
        sup = (i + 1) / k
        termino = (observadas[i] - esperada) ** 2 / esperada
        chi2 += termino
        print(f"   {i:>2}     [{inf:4.2f} , {sup:4.2f})    {observadas[i]:>6}   {esperada:>8.1f}     {termino:>8.4f}")
    print("  " + "-" * 56)

    gl = k - 1
    chi2_critico = CHI2_TABLA_005.get(gl)

    print(f"\n   N (cantidad de numeros) : {n}")
    print(f"   k (clases)              : {k}")
    print(f"   Grados de libertad (k-1): {gl}")
    print(f"   Chi2 calculado          : {chi2:.4f}")
    if chi2_critico is not None:
        print(f"   Chi2 de tabla (a={alfa}) : {chi2_critico}")
        if chi2 <= chi2_critico:
            print(f"\n   RESULTADO: chi2 ({chi2:.4f}) <= tabla ({chi2_critico})")
            print(f"   => NO se rechaza H0. El generador PASA la prueba de uniformidad.\n")
        else:
            print(f"\n   RESULTADO: chi2 ({chi2:.4f}) > tabla ({chi2_critico})")
            print(f"   => Se rechaza H0. El generador NO pasa la prueba.\n")
    else:
        print(f"   (No hay valor de tabla precargado para gl={gl}; agregalo a CHI2_TABLA_005)\n")

    return chi2


if __name__ == "__main__":
    print("=" * 60)
    print("  PRUEBA DE UNIFORMIDAD CHI-CUADRADO")
    print("  Generador Congruencial Lineal Mixto (random_propio.py)")
    print("=" * 60)
    prueba_uniformidad(n=10000, k=10)
