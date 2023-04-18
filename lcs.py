class LCS:
    def process(s: str, t: str) -> str:
        """두 문자열 s와 t의 최장 공통 부분 수열(Longest Common Subsequence, LCS)을 Dynamic Programming을 이용하여 구하는 인스턴스입니다.

        인스턴스의 실행 알고리즘은 아래와 같습니다.
        
        - 두 문자열 s와 t의 길이를 각각 sLength와 tLength로 정의합니다.
        - sLength + 1 * tLength + 1 크기의 2차원 배열 dp를 생성합니다. 이 배열은 LCS를 저장하기 위한 배열입니다. dp[i][j]는 문자열 s의 i번째까지, 문자열 t의 j번째까지의 LCS의 길이를 저장합니다.
        - 반복문을 이용하여 dp 배열을 채웁니다. s와 t의 각 문자를 비교하면서 LCS를 구합니다. 문자가 같을 경우, 대각선 위의 dp값에 1을 더해 현재 위치의 dp값을 저장합니다. 문자가 다를 경우, 좌측과 위쪽 중 큰 값을 현재 위치의 dp값으로 저장합니다.
        - 역추적을 통해 LCS를 구합니다. dp[sLength][tLength]에서부터 시작하여 좌측과 위쪽을 차례대로 비교하면서 공통 문자열을 추출합니다.

        시간 복잡도는 O(nm) 입니다.
        """
        from collections import deque # 덱 모듈을 import
        result = deque() # 결과값을 저장할 덱 생성
        sLength, tLength = len(s), len(t) # 문자열 s와 t의 길이를 구함
        dp = [[0 for _ in range(tLength + 1)] for _ in range(sLength + 1)] # LCS(Longest Common Sequence)을 구할 dp 테이블 생성
        # LCS를 구하는 반복문
        for i in range(1, sLength + 1):
            for j in range(1, tLength + 1):
                if s[i - 1] == t[j - 1]: # s[i - 1]과 t[j - 1]이 같으면
                    dp[i][j] = dp[i - 1][j - 1] + 1 # 대각선 위 값에서 1을 더한 값을 저장
                else: # s[i - 1]과 t[j - 1]이 다르면
                    dp[i][j] = max(dp[i][j - 1], dp[i - 1][j]) # 좌측과 위쪽 중 큰 값을 저장
        si, ti = sLength, tLength
        while True: # LCS 역추적
            # 현재 위치에서 좌측과 위쪽 모두 값이 다르면 공통 문자열이므로 덱에 추가하고 좌측 위쪽으로 이동
            if dp[si - 1][ti] != dp[si][ti] and dp[si][ti - 1] != dp[si][ti]:
                result.appendleft(t[ti - 1])
                si, ti = si - 1, ti - 1
            else:
                if dp[si - 1][ti] == dp[si][ti]: # 좌측 값이 큰 경우 좌측으로 이동
                    si -= 1
                elif dp[si][ti - 1] == dp[si][ti]: # 위쪽 값이 큰 경우 위쪽으로 이동
                    ti -= 1
            if si == 0 or ti == 0: # 시작 위치(0, 0)에 도달하면 종료
                break
        # 덱에 저장된 문자열을 이어붙인 후 반환
        return ''.join(map(str, result))
    def getDPTable(s: str, t: str) -> str:
        dp = [[0 for _ in range(len(s) + 1)] for _ in range(len(t) + 1)]
        for i in range(1, len(t) + 1):
            for j in range(1, len(s) + 1):
                dp[i][j] = dp[i - 1][j - 1] + 1 if s[j - 1] == t[i - 1] else max(dp[i][j - 1], dp[i - 1][j])
        return '\n'.join([
            '-  i  ' + '  '.join(map(str, range(len(s) + 1))),
            'j  -  -  ' + '  '.join(s),
            *[(f'{i}  {"-" if i == 0 else t[i - 1]}  ' + '  '.join(map(str, dp[i]))) for i in range(len(t) + 1)]
        ])
    def processWithHirschBurg(s: str, t: str) -> str:
        def hirschburg(s: str, sLength1: int, sLength2: int, t: str, tLength1: int, tLength2: int) -> str:
            ret, maxValue = '', -float('inf')
            S, T = sLength1 + sLength2 >> 1, 0
            if sLength1 == sLength2:
                return ''
            if sLength1 + 1 == sLength2:
                for i in range(tLength1 + 1, tLength2 + 1):
                    if s[sLength2] == t[i]:
                        return ret + t[i]
                return ''
            for i in range(tLength1, tLength2 + 1):
                LCS1[0][i] = LCS1[1][i] = LCS2[0][i] = LCS2[1][i] = 0
            for i in range(sLength1 + 1, S + 1):
                for j in range(tLength1 + 1, tLength2 + 1):
                    LCS1[i & 1][j] = LCS1[i + 1 & 1][j - 1] + 1 if s[i] == t[j] else max(LCS1[i + 1 & 1][j], LCS1[i & 1][j - 1])
            for i in range(sLength2 - 1, S - 1, -1):
                for j in range(tLength2 - 1, tLength1 - 1, -1):
                    LCS2[i & 1][j] = LCS2[i + 1 & 1][j + 1] + 1 if s[i + 1] == t[j + 1] else max(LCS2[i + 1 & 1][j], LCS2[i & 1][j + 1])
            for i in range(tLength1, tLength2 + 1):
                if LCS1[S & 1][i] + LCS2[S & 1][i] > maxValue:
                    maxValue = LCS1[S & 1][i] + LCS2[S & 1][i]
                    T = i
            return hirschburg(s, sLength1, S, t, tLength1, T) + hirschburg(s, S, sLength2, t, T, tLength2)
        sLength, tLength = len(s), len(t)
        LCS1 = [[0 for _ in range(sLength << 1)] for _ in range(2)]
        LCS2 = [[0 for _ in range(tLength << 1)] for _ in range(2)]
        s = ' ' + s
        t = ' ' + t
        return hirschburg(s, 0, sLength, t, 0, tLength)
    def processWithBitset(s: str, t: str) -> str:
        def bitset(t: str, ret: int) -> int:
            for i in range(len(t)):
                d = cnt = 0
                curT = t[i:] + t[:i]
                for iter in curT:
                    x = d | sArray[ord(iter) - ord('a')]
                    d = x & (x ^ (x - ((d << 1) | 1)))
                while d:
                    cnt += d & 1
                    d >>= 1
                ret = max(ret, cnt)
            return ret
        sArray = [0 for _ in range(26)]
        for i in range(len(s)):
            sArray[ord(s[i]) - ord('a')] |= (1 << i)
        return bitset(''.join(reversed(t)), bitset(t, 0))
