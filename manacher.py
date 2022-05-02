def manacher(s):
    s = '　' + '　'.join(s) + '　'
    n = len(s)
    a = [0 for _ in range(n)]
    r = p = 0
    for i in range(n):
        if i <= r:
            a[i] = min(a[p * 2 - i], r - i)
        else:
            a[i] = 0
        while i - a[i] - 1 >= 0 and i + a[i] + 1 < n and s[i - a[i] - 1] == s[i + a[i] + 1]:
            a[i] += 1
        if r < i + a[i]:
            r = i + a[i]
            p = i
    return max(a)
