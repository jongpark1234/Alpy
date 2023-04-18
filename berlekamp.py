class BerlekampMassey:
    def __init__(self, modulo: int=10 ** 9 + 7):
        self.MOD = modulo
    def __resize(self, numlist: list[int], idx: int) -> list[int]:
        """크기가 idx인 리스트를 반환하는 인스턴스입니다.

        크기가 idx인 리스트를 반환합니다. 만약 numlist의 길이가 idx보다 작으면, numlist를 반환합니다.
        numlist의 길이가 idx보다 크다면, 리스트 뒤에 0을 추가하여 크기를 조정합니다."""
        return numlist[:idx] if idx <= len(numlist) else numlist + [0 for _ in range(idx - len(numlist))]
    def __multiply(self, v1: list[int], v2: list[int], rec: list[int]) -> list[int]:
        """Berlekamp-Massey 알고리즘에서 사용되는 __multiply 인스턴스입니다.
        
        여기서 v, w는 같은 길이를 가지는 리스트이며, 각각 다항식을 나타냅니다.
        이 두 다항식을 곱한 결과를 반환합니다.

        먼저 t를 0으로 초기화합니다. 그리고 v와 w의 각 항을 곱한 값을 t의 인덱스 i + j에 더합니다.
        이후 rec 리스트를 사용하여 거꾸로 추적하며 역원을 적용합니다.
        이 과정에서는 t의 각 항에 rec 리스트의 원소를 곱한 값을 그 앞 항목에 더해줍니다.

        마지막으로 self.__resize 함수를 사용하여 리스트의 길이를 맞춰줍니다."""
        vLength = len(v1)
        t = [0 for _ in range(vLength << 1)] # t를 0으로 수행한다.
        # 행렬 곱셈을 수행한다.
        for i in range(vLength):
            for j in range(vLength):
                t[i + j] += v1[i] * v2[j] % self.MOD
        # 거꾸로 추적하며 역원을 적용한다.
        for i in range((vLength << 1) - 1, vLength - 1, -1):
            for j in range(1, vLength + 1):
                t[i - j] += t[i] * rec[j - 1] % self.MOD
        return self.__resize(t, vLength) # 리스트의 길이를 조절하고 반환
    def __berlekampMassey(self, numlist: list[int]) -> list[int]:
        """입력으로 주어진 숫자 배열의 최소 선형 규칙을 찾아서 반환하는 인스턴스입니다.
        
        Berlekamp-Massey 알고리즘의 성질을 이용하여 다음 숫자를 예측하고, 예측한 숫자와
        다음 숫자가 일치하지 않으면 계수를 수정하여 다음 예측에 반영한다.
        
        이 과정을 반복하여 최소 선형 규칙을 찾는다."""
        ls, cur = [], [] # ls: 마지막으로 저장된 다항식, cur: 현재 다항식.
        for i in range(len(numlist)):
            t = 0
            for j in range(len(cur)):
                t = (t + numlist[i - j - 1] * cur[j]) % self.MOD # 현재 다항식을 이용하여 t를 계산한다.
            if (t - numlist[i]) % self.MOD == 0: # t가 현재 수열 numlist[i]와 같으면 다음 수열 값을 계산
                continue
            if not cur: # 현재 다항식이 비어있다면 초기화
                cur = self.__resize(cur, i + 1)
                lf, ld = i, (t - numlist[i]) % self.MOD # lf: 마지막으로 저장된 위치, ld: 마지막 계수
                continue
            k = -(numlist[i] - t) * pow(ld, self.MOD - 2, self.MOD) % self.MOD # 다음 계수 k 계산
            c = [0 for _ in range(i - lf - 1)] + [k] + [-j * k % self.MOD for j in ls] # 다항식을 계산한다.
            if len(c) < len(cur):
                c = self.__resize(c, len(cur))
            for j in range(len(cur)):
                c[j] = (c[j] + cur[j]) % self.MOD # 다음 다항식을 계산한다.
            if i - lf + len(ls) >= len(cur): # 현재 다항식의 크기보다 크다면 업데이트
                ls, lf, ld = cur, i, (t - numlist[i]) % self.MOD
                # 마지막으로 저장된 다항식을 업데이트하고, lf와 ld도 업데이트
            cur = c[:] # 다음 다항식을 현재 다항식으로 설정
        return list(map(lambda x: (x % self.MOD + self.MOD) % self.MOD, cur))
    def __getNth(self, rec: list[int], numlist: list, idx: int) -> int:
        """__getNth 인스턴스는 피보나치 수열과 같이 이전 값들을 이용해 다음 값을 계산하는 문제에서 특정 인덱스에 해당하는 값을 구하는 인스턴스입니다.
        rec은 Berlekamp-Massey 알고리즘을 통해 구한 재귀식의 계수를 저장한 리스트입니다.
        numlist는 이전 값들의 리스트이며, idx는 구하고자 하는 값의 인덱스입니다.
        
        먼저, 초기 벡터 s는 [1, 0, 0, ..., 0]으로 설정됩니다.
        t는 초기 변환 행렬로서, m=1인 경우 rec의 첫 번째 값만을 원소로 갖는 벡터 [rec[0], 0, ..., 0]가 됩니다.
        이후 t는 __multiply 메서드를 이용하여 제곱되며, s는 필요한 경우 변환 행렬과 곱해져 갱신됩니다.
        
        idx가 0이 될 때까지 위의 과정을 반복하고, 최종적으로 s와 numlist를 곱한 값의 합을 반환합니다."""
        m = len(rec)
        s = [1] + [0 for _ in range(m - 1)] # 초기 벡터
        t = [0, 1] + [0 for _ in range(m - 2)] if m != 1 else [rec[0]] + [0 for _ in range(m - 1)] # 변환 행렬
        while idx:
            if idx & 1:
                s = self.__multiply(s, t, rec) # s에 변환 행렬 t를 곱해 갱신
            t = self.__multiply(t, t, rec) # t를 제곱하여 갱신
            idx >>= 1 # idx를 오른쪽으로 1비트 이동
        return sum(s[i] * numlist[i] % self.MOD for i in range(m)) % self.MOD # s와 numlist를 곱한 값의 합을 반환
    def process(self, numlist: list[int], idx: int) -> int:
        return numlist[idx] if idx < len(numlist) else 0 if not (v := self.__berlekampMassey(numlist)) else self.__getNth(v, numlist, idx)
