from verify import *
def primetest(n):
    if n == 2:
        return True
    if n < 2 or not n & 1:
        return False
    d = n >> 1
    r = 1
    while not d & 1:
        d >>= 1
        r += 1
    numlist = [2, 7, 61] if n < 4759123141 else [2, 325, 9375, 28178, 450775, 9780504, 1795265022]
    return all(verify(i, n, r) for i in numlist)
