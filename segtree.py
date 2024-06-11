class SegmentTree:
    """바텀-업 방식의 세그먼트 트리를 구현한 클래스입니다. 포인트 업데이트 및 구간 쿼리를 지원합니다."""

    def __init__(self, values: list[int], merge = min):
        """
        세그먼트 트리를 초기화합니다.

        세그먼트 트리는 주어진 값들을 기반으로 바텀-업 방식으로 구축됩니다.
        트리 배열은 입력 값 리스트의 두 배 크기로 만들어지며, 후반부는 입력 값들로 채워지고
        전반부는 병합 함수에 의해 계산된 값들로 채워집니다.

        Args:
            values (list[int]): 세그먼트 트리를 초기화하는 데 사용할 값들의 리스트
            merge (Callable, optional): 두 값을 병합하는 데 사용할 함수. 기본값은 min.

        Attributes:
            _size (int): 입력 값들의 개수입니다.
            _tree (list[int]): 세그먼트 트리 구조를 저장하는 리스트입니다.
            _merge (callable): 두 값을 병합하는 데 사용할 함수입니다.
        """

        # 입력 값을 새로운 리스트로 복사
        l = list(values)

        # 입력 값의 크기
        self._size = len(l)

        # 트리 배열을 입력값을 2배로 늘려 제작
        self._tree = l + l

        # 병합 함수 저장
        self._merge = merge

        # bottom-up 방식으로 세그먼트 트리 구축
        for i in range(self._size - 1, 0, -1):
            self._tree[i] = merge(self._tree[i * 2], self._tree[i * 2 + 1])

    def set(self, pos: int, value: int):
        """
        세그먼트 트리에서 특정 위치의 값을 업데이트합니다.
        주어진 위치의 값을 업데이트하고, 그에 따라 세그먼트 트리의 상위 노드들을 갱신합니다.

        Args:
            pos (int): 업데이트할 값의 위치 (0부터 시작).
            value (int): 새로 설정할 값.
        """

        # 위치에 해당하는 트리 배열의 인덱스 갱신
        idx = pos + self._size

        # 루트 노드에 도달할 때까지
        while idx:

            # 현재 위치에 값 설정
            self._tree[idx] = value

            # 현재 값을 형제와 병합 ( 왼쪽 자식인 경우와 오른쪽 자식인 경우로 나뉘어짐)
            value = (self._merge(self._tree[idx - 1], value) if idx & 1 else self._merge(value, self._tree[idx + 1]))

            # 부모 노드로 이동
            idx >>= 1

    def get(self, pos: int) -> int:
        """
        세그먼트 트리에서 주어진 특정 위치의 값을 반환합니다.

        Args:
            pos (int): 값을 가져올 위치 (0부터 시작).

        Returns:
            Node: 지정된 위치의 값.
        """

        # 주어진 위치의 값을 반환
        return self._tree[pos + self._size]

    def query(self, beg: int, end: int) -> int:
        """
        [beg, end) 구간의 값을 쿼리합니다. (end는 포함되지 않습니다).

        주어진 구간의 값을 병합 함수에 따라 병합한 결과를 반환합니다.

        Args:
            beg (int): 쿼리할 구간의 시작 위치 (0부터 시작).
            end (int): 쿼리할 구간의 끝 위치 (0부터 시작, 포함되지 않음).

        Returns:
            Node: 지정된 구간의 값들을 병합한 결과.
        """

        # 구간이 단일 노드일 경우 값을 바로 반환
        if end == beg + 1:
            return self._tree[beg + self._size]
        
        # 왼쪽 및 오른쪽 포인터
        l, r = beg + self._size + 1, end + self._size - 2

        # 왼쪽 끝과 오른쪽 끝의 결과
        ret_l, ret_r = self._tree[l - 1], self._tree[r + 1]

        # 구간 탐색
        while l <= r:

            # l이 오른쪽 자식일 경우 결과에 포함
            if l & 1:
                ret_l = self._merge(ret_l, self._tree[l])

            # r이 왼쪽 자식일 경우 결과에 포함
            if ~r & 1:
                ret_r = self._merge(self._tree[r], ret_r)

            # 다음 구간으로 이동
            l, r = (l + 1) >> 1, (r - 1) >> 1

        # 최종 결과를 병합하여 반환
        return self._merge(ret_l, ret_r)