class FenwickTree:
    """
    구간 합 쿼리를 효율적으로 처리하기 위한 펜윅 트리 자료구조 입니다.

    모든 메서드는 1-based indexing으로 구현되었습니다.

    다만 초기화 배열은 0-based indexing을 사용해야 합니다.
    """

    def __init__(self, numlist: list[int]):
        """
        주어진 정수 리스트로 펜윅 트리를 초기화합니다.

        Args:
            numlist (list[int]): 펜윅 트리를 초기화할 정수 리스트. ( require 0-based array )
        """

        # 입력 리스트의 크기
        self._size = len(numlist)

        # 입력된 리스트
        self._arr = numlist[:]

        # 펜윅 트리 구조
        self._tree = numlist[:]
        
        # 펜윅 트리 구성
        for idx, num in enumerate(self._tree):

            # 현재 노드 i에 대해, 다음 노드의 인덱스가 배열 크기를 초과하지 않는지 확인
            if (node := self._next(idx)) < self._size:

                # 인덱스를 계산하여 부분 합을 누적함
                self._tree[node] += num

    def update(self, idx: int, x: int) -> None:
        """
        주어진 인덱스의 값을 x만큼 업데이트합니다.

        Args:
            idx (int): 업데이트할 인덱스. ( 1 <= idx <= n )
            x (int): 주어진 인덱스의 원소에 더할 값.
        """

        # 0-based indexing을 위해 1 차감
        idx -= 1

        # 원본 리스트 업데이트
        self._arr[idx] += x

        # 현재 위치부터 펜윅 트리의 말단까지 노드를 업데이트
        while idx < self._size:

            # 현재 위치의 노드에 변경할 값 x를 더함
            self._tree[idx] += x

            # 다음 노드로 이동
            idx = self._next(idx)
    
    def set(self, idx: int, x: int) -> None:
        """
        주어진 인덱스의 값을 x로 업데이트합니다.

        Args:
            idx (int): 업데이트할 인덱스. ( 1 <= idx <= n )
            x (int): 주어진 인덱스의 원소에 대입할 값.
        """

        # 변경할 값과 기존 값 간의 차이를 계산한 뒤 이를 더하는 식으로 계산
        self.update(idx, x - self._arr[idx - 1])

    def query(self, start: int, end: int) -> int:
        """
        sum(arr[start - 1], ..., arr[end - 1])을 계산합니다.

        Args:
            start (int): 구간의 시작 인덱스. ( 1 <= start <= n)
            end (int): 구간의 끝 인덱스. ( 1 <= end <= n)

        Returns:
            int: 지정된 구간의 원소들의 합.
        """

        return self.get(end) - self.get(start - 1)
    
    def get(self, idx: int) -> int:
        """
        sum(arr[0], ..., arr[idx - 1])를 계산합니다.

        Args:
            idx (int): 구간의 끝 인덱스 ( 1 <= idx <= n )
        
        Returns:
            int: idx까지 구간의 원소들의 합.
        """
        ret = 0

        # 0-based indexing을 위해 1 차감
        idx -= 1

        # idx 까지의 원소들의 합 계산
        while idx >= 0:

            # 결과값에 해당 노드값 더하기
            ret += self._tree[idx]

            # 이전 노드로 이동
            idx = self._prev(idx)

        return ret
    
    def _prev(self, idx: int) -> int:
        """
        주어진 인덱스의 노드의 이전 노드의 인덱스를 계산합니다.

        Args:
            idx (int): 현재 노드의 인덱스.
        
        Returns:
            int: 이전 노드의 인덱스.
        """

        return (idx & (idx + 1)) - 1

    def _next(self, idx: int) -> int:
        """
        주어진 인덱스의 노드의 다음 노드의 인덱스를 계산합니다.

        Args:
            idx (int): 현재 노드의 인덱스.
        
        Returns:
            int: 다음 노드의 인덱스.
        """
        
        return idx | (idx + 1)