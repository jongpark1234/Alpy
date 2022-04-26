from math import isqrt
def sieve(n):
    if n < 3:
        return [2] if n == 2 else []
    size = (n - 3) // 2
    tlb = [True for _ in range(size + 1)]
    for i in range(isqrt(n - 3) // 2 + 1):
        if tlb[i]:
            e = i * 2 + 3
            s = e * (i + 1) + i
            tlb[s::e] = [False for _ in range((size - s) // e + 1)]
    return [2] + [i * 2 + 3 for i, j in enumerate(tlb) if j]
