class Multiply:
    @staticmethod
    def process(a: list[int], b: list[int]) -> list[int]:
        """decimal 모듈의 C/CFFI 버전은 
        임의의 정밀도로 올바르게 자리 올림 되는 십진 부동 소수점 산술을 위한
        고속 libmpdec 라이브러리를 통합합니다.

        중간 크기의 숫자에는 Karatsuba Multiplication을 사용하고,
        매우 큰 숫자에는 수론적 변환(Number Theoretic Transform)을 사용합니다.
        """
        
        # 필요한 요소들을 import 합니다.
        from decimal import setcontext, Decimal, Context, MAX_EMAX, MAX_PREC

        # Decimal 연산의 정밀도와 최대 지수를 설정합니다.
        setcontext(Context(prec=MAX_PREC, Emax=MAX_EMAX))

        # 입력된 리스트들의 길이와 각 리스트의 최대 값에 따라 연산 결과의 자릿수를 계산합니다.
        digit = len(str(min(len(a), len(b)) * max(a) * max(b)))

        # 형식 문자열을 설정합니다. 연산 결과의 자릿수를 반영합니다.
        f = f'0{digit}d'

        # 리스트의 각 요소를 Decimal로 변환합니다.
        a_dec = Decimal(''.join(format(x, f) for x in a))
        b_dec = Decimal(''.join(format(x, f) for x in b))

        # 두 Decimal 숫자값을 곱하여 결과를 얻습니다. 
        c_dec = a_dec * b_dec

        # 최종 결과의 자릿수를 계산합니다.
        total_digit = digit * (len(a) + len(b) - 1)

        # 자릿수에 맞게 0을 채웁니다.
        c = format(c_dec, f'0{total_digit}f')

        # 계산된 문자열을 digit만큼씩 잘라 각 부분을 정수로 변환하여 리스트로 반환합니다.
        return [int(c[i:i + digit]) for i in range(0, total_digit, digit)]