def fibonacci(n):
    if n < 0:
        return None
    seq = {0: 0, 1: 1}
    s = [(n, n)]
    while s[-1][0]:
        s.append(((s[-1][0] - 1) // 2, (s[-1][1] + 1) // 2))
    for a, b in s[::-1]:
        for k in range(a, b + 1):
            if k not in seq:
                seq[k] = (seq[k // 2] ** 2 + seq[k // 2 + 1] ** 2) if k & 1 else (seq[k // 2] ** 2 + 2 * seq[k // 2] * seq[k // 2 - 1])
    return seq[n]
print(fibonacci(int(input())))