class Primetest:
    def __verify(a: int, n: int, s: int) -> bool:
        """Miller-Rabin Primality Test를 구현하는 verify 인스턴스입니다.

        a ^ (n - 1) ≡ 1 (mod n)을 만족하지 않는 a가 적어도 1/4 이하임을 이용해 n이 소수가 아닌 경우 거의 확실하게 판별할 수 있습니다.
        __verify 인스턴스는 이러한 성질을 이용하여 a 값이 주어졌을 때 n이 소수인지 아닌지 추측합니다.

        n - 1 = 2 ^ s * d (단, d는 홀수) 로 분해한 뒤, a ^ d mod n 값 x를 구합니다.
        a ^ d ≡ 1 (mod n) 이거나, a ^ (2 ^ r * d) ≡ -1 (mod n) 인 경우 True를 반환합니다.
        그 외의 경우 s번 반복하여 a ^ ((2 ^ i) * d) mod n 값을 계산하고, 1이 나오는 경우 False를 반환하고, -1이 나오는 경우 True를 반환합니다.
        모든 반복에서 -1이 나오지 않은 경우 n이 소수가 아니라고 판단합니다."""
        if a >= n: # a가 n보다 큰 경우 a를 n으로 나눈 나머지를 사용하여 계산
            a %= n
        if a < 2: # a가 2 미만인 경우 예외 처리하여 True 반환
            return True
        d = n >> s # n - 1 = 2 ^ s * d (단, d는 홀수) 로 분해
        x = pow(a, d, n) # a ^ d mod n 값을 구함
        if x == n - 1: # a ^ (2 ^ r * d) ≡ -1 (mod n) 인 경우 True 반환
            return True
        if x == 1: # a ^ d ≡ 1 (mod n) 인 경우 True 반환
            return True
        for _ in range(s): # s번 반복하여 a ^ ((2 ^ x) * d) mod n 값을 계산
            x = pow(x, 2, n)
            if x == 1: # 1이 나오는 경우 False 반환
                return False
            if x == n - 1: # -1이 나오는 경우 True 반환
                return True
        return False # 위의 두 경우가 아닌 경우 False 반환
    def process(self, n):
        if n == 2: # 2 반례 처리
            return True
        if n < 2 or ~n & 1: # 2 미만인 수, 짝수 반례 처리
            return False
        r, d = 1, n >> 1
        while ~d & 1:
            d >>= 1
            r += 1
        return all(self.__verify(i, n, r) for i in ([2, 7, 61] if n < 4759123141 else [2, 325, 9375, 28178, 450775, 9780504, 1795265022]))
