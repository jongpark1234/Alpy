from primetest import Primetest
from random import randrange
from math import gcd

class Factorize:
    """
    Pollard's Rho 알고리즘을 구현한 클래스입니다.
     
    이 클래스는 주어진 정수를 소인수분해하여 소인수 중 하나를 찾는 기능을 제공합니다.

    Pollard's Rho 알고리즘은 효율적인 소인수분해 방법 중 하나로, 무작위성을 활용하여 소인수를 찾아내는 방식으로 작동합니다.
    
    이 클래스는 주어진 정수에 대해 Pollard's Rho 알고리즘을 적용하여 소인수를 찾는 메소드를 제공합니다.
    """

    def _f(x: int, a: int, n: int) -> int:
        """
        f(x)=x^2+a(mod n) 꼴의 이차다항식을 구현한 메소드입니다.

        Args:
            x (int): 계산에 사용되는 정수 값.
            a (int): 이차 다항식의 상수항.
            n (int): 모듈러 연산에 사용되는 정수 값.

        Returns:
            int: 이차 다항식 f(x) = x^2 + a (mod n) 을 계산한 값.
        """
        return (pow(x, 2) + a) % n

    def __pollard_rho(self, n: int) -> int:
        """
        Pollard's Rho 알고리즘을 사용하여 소인수를 찾는 메소드입니다.

        Args:
            n (int): 소인수분해할 정수.
        
        Returns:
            int: 주어진 정수 n의 소인수 중 하나를 나타내는 정수 값.
        """

        # 임의의 시작값 x와 c를 선택
        x = randrange(1, n)
        c = randrange(1, n)
        y, g = x, 1

        # 임의의 수가 n과 1이 아닌 공약수를 가질 때까지 반복
        while g == 1:

            # x = f(x)
            x = self._f(x, c, n)

            # y = f(f(y))
            y = self._f(self._f(y, c, n), c, n)

            # x와 y 사이 차의 최대공약수를 계산
            g = gcd(abs(x - y), n)

        # 만약 g가 n과 같으면, 새로운 x와 c를 선택하여 다시 시도
        if g == n:
            return self.__pollard_rho(n)
        
        # g가 n과 다르면 찾은 소인수를 반환
        return g

    def factorize(self, n: int) -> list[int]:
        """
        주어진 정수 n을 소인수분해하는 메소드

        Args:
            n (int): 소인수분해할 정수.

        Returns:
            list[int]: n의 소인수 리스트.
        """

        # n이 1이면 빈 리스트 반환
        if n == 1:
            return []
        
        # n이 짝수인 경우, 2를 소인수로 추가하고 n을 반으로 나눈 값을 재귀적으로 소인수분해
        if ~n & 1:
            return [2] + self.factorize(n >> 1)
        
        # n이 소수인 경우, n을 반환
        if Primetest().process(n):
            return [n]
        
        # Pollard's Rho 알고리즘을 사용하여 n의 소인수 찾기
        f = self.__pollard_rho(n)
        
        # 찾은 소인수로 n을 나누고 재귀적으로 소인수분해 진행
        return self.factorize(f) + self.factorize(n // f)
    

print(Factorize().factorize(52341243))