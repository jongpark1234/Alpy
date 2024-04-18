class Sieve:
    def prime_list(a: int) -> list[int]:
        """
        주어진 범위 내의 소수를 찾아 리스트로 반환합니다.
        
        Args:
            a (int): 소수를 찾을 범위입니다. [1, a] 까지의 소수 리스트를 반환하게 됩니다.
        
        Returns:
            list[int]: 지정된 범위 내의 소수 목록을 반환합니다.
        """
        from math import isqrt
        
        # 범위의 시작과 끝을 결정
        l, r = 1, a + 1
        
        # 범위가 5보다 작으면 2와 3을 반환
        if r < 5:
            return [i for i in range(l, r) if i in (2, 3)]
        
        # 범위의 끝을 조정
        n = r + 6 - r % 6
        
        # 잠재적인 소수를 나타내는 True 값을 갖는 체 배열을 초기화
        # 2,3-wheel factorization 기법을 사용
        sieve = [False] + [True] * (n // 3 - 1)
        
        # 에라토스테네스의 체 알고리즘을 적용하여 합성수 표시
        for i in range(isqrt(n) // 3 + 1):
            if sieve[i]:
                dist, ii, idx = (k := 1 | 3 * i + 1) * 2, k * k, k * (k + 4 - 2 * (i & 1))
                sieve[ii // 3::dist] = [False] * ((n // 6 - ii // 6 - 1) // k + 1)
                sieve[idx // 3::dist] = [False] * ((n // 6 - idx // 6 - 1) // k + 1)
        
        # 지정된 범위 내의 소수 목록 생성 후 반환
        return ([p for p in (2, 3) if p >= l] + [1 | 3 * i + 1 for i in range((l | 1) // 3, n // 3 - 2 + (r % 6 > 1)) if sieve[i]])