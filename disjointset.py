class DisjointSet:
    """경로 압축(path compression)과 크기에 따른 합집합(union-by-size)을 사용하는
    Integer를 위한 Disjoint Set(서로소 집합)을 구현한 클래스입니다.
    
    Disjoint Set은 여러 집합들을 효율적으로 관리하기 위한 자료구조로, 각 원소들이 서로소인 집합들의 집합을 나타냅니다."""

    def __init__(self, size: int):

        # 각 원소의 부모를 저장하는 리스트.
        # 초기에는 모든 원소의 부모를 -1로 설정하여 각각이 독립 집함임을 나타냄.
        self._parent = [i for i in range(size)]
        self._size = [1 for _ in range(size)]

    def union(self, x: int, y: int) -> int:
        """
        주어진 두 원소 x와 y가 속한 집합을 합칩니다.
        각 원소의 루트(root)를 찾은 후, 두 루트가 같으면 이미 같은 집합에 속해있으므로 아무 작업도 하지 않고 해당 루트를 반환합니다.
        
        그렇지 않다면, 두 루트 중 크기가 더 작은 집합을 크기가 더 큰 집합에 합칩니다. 이때, 합친 집합의 루트를 반환합니다.

        Args:
            x (int): 각각이 속한 집합을 합칠 두 원소 중 첫번째 원소입니다.
            y (int): 각각이 속한 집합을 합칠 두 원소 중 두번째 원소입니다.

        Returns:
            int: 합쳐진 집합의 루트 노드를 반환합니다.
        """

        # 각 원소 x와 y가 속한 집합의 root 노드를 찾음
        root_x, root_y = self.find(x), self.find(y)

        # 이미 같은 집합에 속해있다면 root를 반환
        if root_x == root_y:
            return root_x
        
        # 두 집합을 합치기 위해 크기를 비교하여 더 작은 집합을 더 큰 집합에 붙임
        if self._size[root_x] < self._size[root_y]:
            root_x, root_y = root_y, root_x

        # 합친 집합의 크기를 업데이트하고, 합친 집합의 root를 반환
        self._parent[root_y] = root_x
        self._size[root_x] += self._size[root_y]

        return root_x

    def find(self, x: int) -> int:
        """
        주어진 원소 x가 속한 집합의 루트를 찾습니다.
        경로 압축을 이용하여 x의 부모를 그 집합의 루트로 업데이트하면서 루트를 찾습니다.
        
        마지막으로 찾은 루트를 반환합니다.

        Args:
            x (int): 루트를 찾을 원소입니다.
        
        Returns:
            int: 해당 원소의 루트 노드를 반환합니다.
        """

        # 주어진 원소 x가 속한 집합의 루트를 찾음
        while (p := self._parent[x]) != x:
            
            # 경로 압축을 통해 x의 부모를 해당 집합의 루트로 업데이트
            x, self._parent[x] = p, self._parent[p]

        # 마지막으로 찾은 루트를 반환
        return x