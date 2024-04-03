class Primetest:
    """
    밀러-라빈 소수판별법을 사용하여 주어진 정수가 소수인지 판별하는 기능을 제공하는 클래스입니다.
    """
    def __verify(self, a: int, n: int, s: int) -> bool:
        """
        Miller-Rabin Primality Test를 한 verify 인스턴스입니다.

        a ^ (n - 1) ≡ 1 (mod n)을 만족하지 않는 a가 적어도 1/4 이하임을 이용해 n이 소수가 아닌 경우 거의 확실하게 판별할 수 있습니다 ( probable prime ).

        이러한 성질을 이용하여 a 값이 주어졌을 때 n이 소수인지 아닌지 여부의 추측값을 반환합니다.

        Args:
            a (int): 밀러 라빈 테스트에 사용되는 정수 값. 이 값은 0 이상이어야 합니다.
            n (int): 소수 판별 대상이 되는 정수 값.
            s (int): n - 1을 2^s * d 형태로 분해한 결과의 지수 부분인 s 값. 여기서 d는 홀수입니다.

        Returns:
            bool: 주어진 정수 n이 소수인지 아닌지 여부의 추측값을 반환합니다. True일 경우 n이 소수일 가능성이 높고, False일 경우 n이 합성수일 가능성이 높습니다.
        """

        # a가 n보다 큰 경우 a를 n으로 나눈 나머지를 사용하여 계산
        if a >= n:
            a %= n

        # a가 2 미만인 경우 예외 처리하여 True 반환
        if a < 2:
            return True
        
        # n - 1 = 2 ^ s * d (단, d는 홀수) 로 분해
        d = n >> s

        # a ^ d (mod n) 값을 구함
        x = pow(a, d, n)

        # a ^ (2 ^ r * d) ≡ -1 (mod n) 인 경우 True 반환
        if x == n - 1:
            return True
        
        # a ^ d ≡ 1 (mod n) 인 경우 True 반환
        if x == 1:
            return True
        
        # s번 반복하여 a ^ ((2 ^ x) * d) mod n 값을 계산
        for _ in range(s):
            x = pow(x, 2, n)

            # 1이 나오는 경우 False 반환
            if x == 1:
                return False
            
            # -1이 나오는 경우 True 반환
            if x == n - 1:
                return True

        # 위의 두 경우가 아닌 경우 False 반환
        return False
    
    def process(self, n: int) -> bool:
        """
        주어진 정수 n이 소수인지 판별하는 메소드입니다. 밀러-라빈 소수판별법을 사용합니다.

        Args:
            n (int): 소수 여부를 확인할 정수.

        Returns:
            bool: n이 소수인 경우 True, 합성수인 경우 False를 반환합니다.
        """

        # 2는 소수
        if n == 2:
            return True
        
        # 2 미만의 수 및 짝수는 소수가 아님
        if n < 2 or ~n & 1:
            return False
        
        # n - 1 = 2^r * d (단, d는 홀수) 로 분해
        r, d = 1, n >> 1
        while ~d & 1:
            d >>= 1  # d가 홀수가 될 때까지 2로 나눔
            r += 1   # r은 2^r을 의미

        # 밀러-라빈 소수판별법을 사용하여 소수 여부 확인
        return all(self.__verify(i, n, r) for i in ([2, 7, 61] if n < 4759123141 else [2, 325, 9375, 28178, 450775, 9780504, 1795265022]))