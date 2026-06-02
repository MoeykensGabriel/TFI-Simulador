# ============================================================
#  random_propio.py  -  Generador de numeros pseudoaleatorios
# ------------------------------------------------------------
#  AQUI VA: nuestro propio generador, en vez del de la libreria.
#  Implementa un Generador Congruencial Lineal (GCL):
#
#       X(n+1) = (a * X(n) + c) mod m
#       u = X(n+1) / m        -> numero en [0, 1)
#
#  Constantes "Numerical Recipes" (buen periodo y propiedades):
#       a = 1664525, c = 1013904223, m = 2^32
#
#  Expone las mismas funciones que usamos del modulo random, asi
#  el resto del sistema no necesita cambiar:
#       random(), uniform(a,b), gauss(mu,sigma), randint(a,b)
# ============================================================

import math


class GeneradorCongruencial:
    """Generador Congruencial Lineal (GCL)."""

    def __init__(self, semilla: int = 12345):
        self.a = 1664525
        self.c = 1013904223
        self.m = 2 ** 32
        self.x = semilla % self.m
        self._gauss_guardado = None   # cache para Box-Muller

    def semilla(self, valor: int):
        """Reinicia el generador con una nueva semilla."""
        self.x = valor % self.m
        self._gauss_guardado = None

    def random(self) -> float:
        """Devuelve un U(0,1): el siguiente numero pseudoaleatorio."""
        self.x = (self.a * self.x + self.c) % self.m
        return self.x / self.m

    def uniform(self, a: float, b: float) -> float:
        """Devuelve un U(a,b)."""
        return a + (b - a) * self.random()

    def randint(self, a: int, b: int) -> int:
        """Devuelve un entero uniforme en [a, b] (ambos incluidos)."""
        return a + int(self.random() * (b - a + 1))

    def gauss(self, mu: float, sigma: float) -> float:
        """
        Devuelve un valor Normal(mu, sigma) por el metodo de
        Box-Muller, que transforma dos U(0,1) en dos normales.
        """
        if self._gauss_guardado is not None:
            z = self._gauss_guardado
            self._gauss_guardado = None
            return mu + sigma * z

        u1 = self.random()
        u2 = self.random()
        # Evitar log(0)
        if u1 < 1e-12:
            u1 = 1e-12
        r = math.sqrt(-2.0 * math.log(u1))
        z0 = r * math.cos(2 * math.pi * u2)
        z1 = r * math.sin(2 * math.pi * u2)
        self._gauss_guardado = z1   # guardar el segundo para la proxima
        return mu + sigma * z0


# Instancia global: el resto del sistema usa estas funciones igual
# que usaria las del modulo random.
_gen = GeneradorCongruencial()

def semilla(valor: int):
    _gen.semilla(valor)

def random() -> float:
    return _gen.random()

def uniform(a: float, b: float) -> float:
    return _gen.uniform(a, b)

def randint(a: int, b: int) -> int:
    return _gen.randint(a, b)

def gauss(mu: float, sigma: float) -> float:
    return _gen.gauss(mu, sigma)
