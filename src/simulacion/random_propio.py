import math


class GeneradorCongruencial:

    def __init__(self, semilla: int = 12345):
        self.a = 1664525
        self.c = 1013904223
        self.m = 2 ** 32
        self.x = semilla % self.m
        self._gauss_guardado = None

    def semilla(self, valor: int):
        self.x = valor % self.m
        self._gauss_guardado = None

    def random(self) -> float:
        # x(i+1) = (a*x(i) + c) mod m, u = x/m uniforme en 0,1
        self.x = (self.a * self.x + self.c) % self.m
        return self.x / self.m

    def uniform(self, a: float, b: float) -> float:
        return a + (b - a) * self.random()

    def randint(self, a: int, b: int) -> int:
        return a + int(self.random() * (b - a + 1))

    def gauss(self, mu: float, sigma: float) -> float:
        # box muller transforma dos u(0,1) en dos normales
        if self._gauss_guardado is not None:
            z = self._gauss_guardado
            self._gauss_guardado = None
            return mu + sigma * z

        u1 = self.random()
        u2 = self.random()
        if u1 < 1e-12:
            u1 = 1e-12
        r = math.sqrt(-2.0 * math.log(u1))
        z0 = r * math.cos(2 * math.pi * u2)
        z1 = r * math.sin(2 * math.pi * u2)
        self._gauss_guardado = z1
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
