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
