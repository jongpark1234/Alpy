from disjointset import DisjointSet

class BiconnectedComponent:
    """
    BiconnectedComponent 클래스는 그래프에서 이중 연결된 구성 요소를 찾기 위한 클래스입니다.
    이 클래스는 주어진 노드 수와 엣지 목록을 통해 그래프를 구성하고, DFS를 이용해 각 노드의 깊이를 설정하며, 
    브리지 엣지를 감지하고, 구성 요소를 결합합니다.
    """

    def __init__(self, n: int):
        """
        Args:
            n (int): 그래프의 노드 수
        """

        # 노드의 수
        self.n = n

        # 그래프를 표현하는 인접 리스트
        self.graph = [[] for _ in range(n)]

        # 각 노드의 DFS 방문 시간을 저장하는 리스트
        self.depth = [0 for _ in range(n)]

        # 브리지를 저장하는 리스트
        self.bridge = []

        # 연결된 구성 요소를 관리하는 Disjoint Set
        self.djs = DisjointSet(n)

        # dfs와 edge의 인덱스
        self.dfs_index = self.edge_index = 0
    
    def add_edge(self, u: int, v: int, idx: int = -1) -> None:
        """
        그래프에 엣지를 추가하는 메서드입니다. 주어진 두 노드 u와 v를 엣지로 연결합니다.
        엣지 인덱스가 제공되지 않으면 자동으로 인덱스를 할당합니다.
        
        Args:
            u (int): 엣지의 시작 노드
            v (int): 엣지의 종료 노드
            idx (int): 엣지의 인덱스
        """
        # idx가 -1이면
        if idx == -1:

            # 새 엣지의 인덱스를 현재 edge_index로 설정
            idx = self.edge_index

            # 다음 엣지를 위해 edge_index를 증가
            self.edge_index += 1
        
        # 그래프에 간선 추가
        self.graph[u].append((v, idx))
        self.graph[v].append((u, idx))

    def dfs(self, u: int, idx: int = -1) -> int:
        """
        깊이 우선 탐색(DFS)을 수행하는 메서드입니다. 현재 노드 u에서 시작하여
        그래프를 탐색하고, 각 노드의 깊이를 설정하며, 브리지 엣지를 감지합니다.
        
        Args:
            u (int): DFS를 시작할 노드
            idx (int): 현재 엣지의 인덱스 (기본값은 -1)
        
        Returns:
            int: 현재 노드 u의 DFS 탐색 중 발견된 최소 깊이
        """
        # dfs 탐색 순서 증가
        self.dfs_index += 1

        # 현재 노드 u의 깊이를 dfs_index로 설정한 뒤 반환 값에 저장
        ret = self.depth[u] = self.dfs_index

        # 노드 u에 연결된 모든 노드 v와 엣지 인덱스 i를 탐색
        for v, i in self.graph[u]:

            # 현재 탐색 중인 엣지와 연결된 엣지 i가 동일한 경우 건너뜀
            if idx == i:
                continue

            # 만약 노드 v가 방문되지 않은 경우
            if not self.depth[v]:

                # 노드 v에 대해 dfs를 수행한 값이 노드 u의 깊이보다 큰 경우 u와 v 사이의 엣지가 브리지임을 의미
                if (t := self.dfs(v, i)) > self.depth[u]:
                    self.bridge.append((u, v, i))

                # 그렇지 않은 경우 u와 v를 동일한 구성 요소로 결합
                else:
                    self.djs.union(u, v)
                
                # ret 값을 현재 깊이와 t 값 중 작은 값으로 업데이트
                ret = min(ret, t)
            else:

                # 방문된 노드 v의 깊이와 현재 ret 값 중 작은 값으로 업데이트
                ret = min(ret, self.depth[v])

        # 노드 u의 DFS 탐색 완료 후 값 반환
        return ret

    def get_bcc(self) -> None:
        """
        그래프의 모든 노드를 방문하여 DFS 탐색을 수행하고,
        이중 연결된 구성 요소(Biconnected Components)를 찾는 메서드입니다.
        """

        # 그래프의 모든 노드를 순회
        for i in range(self.n):

            # 현재 노드가 방문되지 않은 경우
            if not self.depth[i]:

                # 해당 노드에서 DFS 탐색 시작
                self.dfs(i)