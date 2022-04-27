# Alpy
알고리즘들의 기본 형태를 Python으로 구현하여 올리는 Repository입니다.

## 현재 진행도
    - 소수 판정 ( 80% )
    - 에라토스테네스의 체 ( 100% )
    - 소인수 분해 ( 70% )
    - 제곱수 분해 ( 100% )
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

함수는 `primetest()`, int 형 정수 하나를 매개변수로 받으며 해당 정수가 소수인지 아닌지 여부를 판별하는 True 또는 False 의 Boolean 값을 반환합니다.

시간복잡도는 ![O(k\log^n)](https://latex.codecogs.com/gif.latex?O%28k%5Clog%5E3n%29) 에 동작합니다. ( 이 때, ![k](https://latex.codecogs.com/gif.latex?k)는 소수 판별법을 몇 회 실행할지 결정하는 인자입니다. )

## 에라토스테네스의 체 ( Sieve of Eratosthenes )
`sieve.py`

2-wheel factorization 기법을 적용하여 에라토스테네스의 체를 작성하였습니다.

함수는 `sieve()`, int 형 정수 하나를 매개변수로 받으며 n 이하의 모든 소수들을 오름차순 정렬된 list 형태로 반환합니다.

시간복잡도는 ![O(n\log\log n)](https://latex.codecogs.com/gif.latex?O%28n%5Clog%5Clog%20n%29) 에 동작합니다.

## 소인수 분해 ( Factorize )
`factorize.py`

pollard-rho 알고리즘을 이용하여 소인수분해를 작성하였습니다.

함수는 `factorize()`, int형 정수 하나를 매개변수로 받으며 n의 소인수들을 정렬되지 않은 list 형태로 반환합니다.

시간복잡도는 ![O(^{4}\sqrt{n})](https://latex.codecogs.com/gif.latex?O%28n%5E%7B%5Cfrac%7B1%7D%7B4%7D%7D%29) 에 동작합니다.

## 제곱수 분해 ( Decompose by Square )
`square.py`

함수는 `square()`, int형 정수 하나를 매개변수로 받으며 n을 이루는 제곱수들을 내림차순 정렬된 list 형태로 반환합니다.

시간복잡도는 ![O(N^{1/4}\sqrt{\ln N})](https://latex.codecogs.com/gif.latex?O%28N%5E%7B1/4%7D%20%5Csqrt%7B%5Cln%20N%7D%29) 에 동작합니다.