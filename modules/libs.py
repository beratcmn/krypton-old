import math
import time


def karesi(x: float):
    return int(x ** 2) if int(x) == x else x ** 2


def kupu(x: float):
    return int(x ** 3) if int(x) == x else x ** 3


def karekok(x: float):
    return int(x ** (1/2)) if int(x) == x else x ** (1/2)


def kupkok(x: float):
    return int(x ** (1/3)) if int(x) == x else x ** (1/3)


def mutlak(x: float):
    return abs(int(x)) if int(x) == x else abs(x)


def bekle(x: int):
    time.sleep(x)


if __name__ == "__main__":
    print(mutlak(-2))
    print(mutlak(-2.4))
