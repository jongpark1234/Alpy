class BerlekampMassey:
    def __init__(self, modulo: int):
        self.MOD = modulo
    def __resize(self, numlist: list[int], idx: int) -> list[int]:
        return numlist[:idx] if idx <= len(numlist) else numlist + [0 for _ in range(idx - len(numlist))]
    def __multiply(self, v: list[int], w: list[int], rec: list[int]) -> list[int]:
        m = len(v)
        t = [0 for _ in range(m << 1)]
        for i in range(m):
            for j in range(m):
                t[i + j] += v[i] * w[j] % self.MOD
        for i in range((m << 1) - 1, m - 1, -1):
            for j in range(1, m + 1):
                t[i - j] += t[i] * rec[j - 1] % self.MOD
        return self.__resize(t, m)
    def __berlekampMassey(self, numlist: list[int]) -> list[int]:
        ls, cur = [], []
        for i in range(len(numlist)):
            t = 0
            for j in range(len(cur)):
                t = (t + numlist[i - j - 1] * cur[j]) % self.MOD
            if (t - numlist[i]) % self.MOD == 0:
                continue
            if not cur:
                cur = self.__resize(cur, i + 1)
                lf, ld = i, (t - numlist[i]) % self.MOD
                continue
            k = -(numlist[i] - t) * pow(ld, self.MOD - 2, self.MOD) % self.MOD
            c = [0 for _ in range(i - lf - 1)] + [k] + [-j * k % self.MOD for j in ls]
            if len(c) < len(cur):
                c = self.__resize(c, len(cur))
            for j in range(len(cur)):
                c[j] = (c[j] + cur[j]) % self.MOD
            if i - lf + len(ls) >= len(cur):
                ls, lf, ld = cur, i, (t - numlist[i]) % self.MOD
            cur = c[:]
        return list(map(lambda x: (x % self.MOD + self.MOD) % self.MOD, cur))
    def __getNth(self, rec: list[int], numlist: list, idx: int) -> int:
        m = len(rec)
        s = [1] + [0 for _ in range(m - 1)]
        t = [0, 1] + [0 for _ in range(m - 2)] if m != 1 else [rec[0]] + [0 for _ in range(m - 1)]
        while idx:
            if idx & 1:
                s = self.__multiply(s, t, rec)
            t = self.__multiply(t, t, rec)
            idx >>= 1
        return sum(s[i] * numlist[i] % self.MOD for i in range(m)) % self.MOD
    def process(self, numlist: list[int], idx: int) -> int:
        return numlist[idx] if idx < len(numlist) else 0 if not (v := self.__berlekampMassey(numlist)) else self.__getNth(v, numlist, idx)
