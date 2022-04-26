def primetest(n):
    def verify(a, n, s):
        if a >= n:
            a %= n
        if a < 2:
            return True
        d = n >> s
        x = pow(a, d, n)
        if x == n - 1:
            return True
        if x == 1: 
            return True
        for _ in range(s):
            x = x * x % n
            if x == 1:
                return False
            if x == n - 1:
                return True
        return False
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
