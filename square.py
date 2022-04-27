def square(n):
    from factorize import factorize
    class Gauss:
        def __init__(self, r, n):
            self.r = r
            self.n = n
        def norm(self):
            return self.r ** 2 + self.n ** 2
        def __floordiv__(a, b):
            def cal(a, b):
                ret = a % b
                if ret < 0:
                    ret += b
                if ret * 2 > b:
                    ret -= b
                return (a - ret) // b
            a1, a2 = a.r, a.n
            b1, b2 = b.r, b.n
            n = b.norm()
            return Gauss(cal(a1 * b1 + a2 * b2, n), cal(a2 * b1 - a1 * b2, n))
        def __mod__(a, b):
            a1, a2 = a.r, a.n
            b1, b2 = b.r, b.n
            q = a // b
            q1, q2 = q.r, q.n
            return Gauss(a1 - q1 * b1 + q2 * b2, a2 - q1 * b2 - q2 * b1)
        def GCD(a, b):
            while b.r or b.n:
                a, b = b, a % b
            return a
    def power(x, y, p):
        r = 1
        x %= p
        while y:
            if y & 1:
                r = (r * x) % p
            y >>= 1
            x = x ** 2 % p
        return r
    def sumTwoSquare1(n):
        if n == 2:
            return [1, 1]
        k = n // 4
        j = 2
        while True:
            a = power(j, k, n)
            if a ** 2 % n == n - 1:
                break
            j += 1
        uc = Gauss.GCD(Gauss(n, 0), Gauss(a, 1))
        return [abs(uc.r), abs(uc.n)]
    def sumTwoSquare2(n):
        s = 1
        primes = set()
        for i in factorize(n):
            if i in primes:
                s *= i
                primes.remove(i)
            else:
                primes.add(i)
        if not primes:
            return [s, 0]
        for i in primes:
            if i % 4 == 3:
                return 'E'
        a, b = s, 0
        for i in primes:
            c, d = sumTwoSquare1(i)
            a, b = a * c + b * d, a * d - b * c
        return [abs(a), abs(b)]
    def sumSquare(n):
        result = 0
        if n == 0:
            return []
        if n % 4 == 0:
            while n % 4 == 0:
                n //= 4
                result += 1
            return list(map(lambda x: x << result, sumSquare(n)))
        if n % 8 == 7:
            return sumSquare(n - 1) + [1]
        ss = sumTwoSquare2(n)
        if ss != 'E':
            res = []
            a, b = ss
            if a:
                res.append(a)
            if b:
                res.append(b)
            return res
        i = 2
        if n % 4 == 3:
            i = 1
        while True:
            ab = sumTwoSquare2(n - i ** 2)
            if ab != 'E':
                return list(ab) + [i]
            i += 2
    return sumSquare(n)
