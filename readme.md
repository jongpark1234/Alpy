# illusion
알고리즘들의 기본 형태를 Python으로 구현하여 올리는 Repository입니다.

## 현재 진행도
    - 소수 판정 ( 50% )
    - 에라토스테네스의 체 ( 0% )
    - 소인수 분해 ( 50% )
    - 제곱수 분해 ( 0% )
    - 누적 합 ( 0% )
    - 세그먼트 트리 ( 0% )
    - 느리게 갱신되는 세그먼트 트리 ( 0% )
    - 고속 푸리에 변환 ( 0% )
    - KMP ( 0% )
    - 접미사 배열 ( 0% )
    - 매내처 ( 0% )
    - 러빈 카프 ( 0% )
    - 트라이 ( 0% )
    - 최장 공통 부분 수열 ( 0% )
    - 가장 긴 증가하는 부분 수열 ( 0% )
    - Lower/Upper_bound ( 0% )

이후 더 추가될 수 있습니다.

## 소수 판정 ( Primality Test )
`primetest.py`

밀러-라빈 소수 테스트를 사용하여 소수 판정을 작성하였습니다.

시간복잡도는 ![O(k\log^n)](https://latex.codecogs.com/gif.latex?O%28k%5Clog%5E3n%29) 에 동작합니다. ( 이 때, ![k](https://latex.codecogs.com/gif.latex?k)는 소수 판별법을 몇 회 실행할지 결정하는 인자입니다. )

## 소인수 분해 ( Factorize )
`factorize.py`

pollard-rho 알고리즘을 이용하여 소인수분해를 작성하였습니다.
pollard-rho 알고리즘 자체는 인수분해 알고리즘이지만, 이를 재귀적으로 1 또는 소수가 나올때까지 인수분해하여 소인수분해를 진행합니다.

시간복잡도는 ![O(^{4}\sqrt{n})](https://latex.codecogs.com/gif.latex?O%28%5E%7B4%7D%5Csqrt%7Bn%7D%29) 에 동작합니다.