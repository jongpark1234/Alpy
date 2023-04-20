from primetest import Primetest
from random import randrange
from math import gcd
def factorize(n):
    def pollard_rho(n):
        x = randrange(1, n)
        c = randrange(1, n)
        y, g = x, 1
        while g == 1:
            x = (x * x + c) % n
            y = (y * y + c) % n
            y = (y * y + c) % n
            g = gcd(abs(x - y), n)
        if g == n:
            return pollard_rho(n)
        return g
    if n == 1:
        return []
    if ~n & 1:
        return [2] + factorize(n >> 1)
    if Primetest.process(n):
        return [n]
    f = pollard_rho(n)
    return factorize(f) + factorize(n // f)
