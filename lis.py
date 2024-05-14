class LIS:
    def process(sequence: list[int]) -> list[int]:
        """한 정수 수열 sequence를 받아 해당 수열의 최장 증가 부분 수열(Longest Increasing Subsequence, LIS)을 구하는 인스턴스입니다.

        구현은 최장 증가 부분 수열(LIS)을 구하는 알고리즘 중 하나인 "Patience Sorting" 알고리즘을 이용하여 구현되었습니다.
        
        시간 복잡도는 O(nlogn)입니다."""

        from collections import deque
        from bisect import bisect_left

        # 수열(sequence)의 길이
        n = len(sequence)

        # dp: LIS 길이 저장용 리스트, lis: LIS 저장용 리스트, ret: 반환할 LIS 저장용 양방향 큐
        dp, lis, ret = [0 for _ in range(n)], [], deque()

        # 수열(sequence)의 각 원소를 하나씩 탐색
        for i in range(n):

            # 만약 탐색한 원소가 LIS의 마지막 원소보다 크거나, 수열의 첫 번째 원소라면
            if i == 0 or lis[-1] < sequence[i]:

                # LIS에 추가
                lis.append(sequence[i])

                # dp 리스트에 해당 인덱스까지의 LIS 길이 저장
                dp[i] = len(lis)

                # 다음 원소 탐색
                continue

            # bisect_left 함수를 이용하여 탐색한 원소가 들어갈 위치(인덱스)를 구함
            idx = bisect_left(lis, sequence[i])

            # 해당 위치에 원소 삽입, dp 리스트에 해당 인덱스까지의 LIS 길이 저장
            lis[idx], dp[i] = sequence[i], idx + 1

        # LIS 길이
        t = len(lis)

        # 수열(sequence)의 끝부터 시작하여
        for i in range(n - 1, -1, -1):
            
            # 만약 해당 원소까지의 LIS 길이가 전체 LIS 길이(t)와 같지 않다면
            if dp[i] ^ t:

                # 다음 원소 탐색 
                continue

            # 양방향 큐에 해당 원소 추가
            ret.appendleft(sequence[i])

            # LIS 길이 감소
            t -= 1

        # deque를 리스트로 변환하여 반환
        return list(ret)
