from collections import deque
class MF:
    def __init__(self, v: int):

        # v개의 정점을 가진 최대 유량 그래프 초기화
        self.size = v

        # 그래프의 인접 리스트
        self.adj = [[] for _ in range(v)]

        # 용량을 저장하는 인접 리스트
        self.cap = [[0 for _ in range(v)] for _ in range(v)]

        # 흐름을 저장하는 인접 리스트
        self.flow = [[0 for _ in range(v)] for _ in range(v)]

        # 각 노드까지의 거리를 저장하는 리스트
        self.depth = [0 for _ in range(v)]

        # 각 노드의 마지막으로 방문한 간선을 저장하는 리스트
        self.last = [0 for _ in range(v)]

    def add_edge(self, u: int, v: int, c: int, d: bool=True):
        """
        정점 'u'에서 정점 'v'로 용량 'c'를 갖는 간선을 추가합니다.
        이 메소드는 간선을 그래프에 추가하고 간선 리스트 'edges'에 저장합니다.
        양방향 간선일 경우 'd'를 False로 설정하여 역방향 간선도 추가합니다.

        Args:
            u (int): 간선의 시작 정점
            v (int): 간선의 도착 정점
            c (int): 간선의 용량
            d (bool, optional): 간선의 방향성 여부, 기본값은 True (단방향 간선)
        """

        # u에서 v로 가는 간선 추가
        self.adj[u].append(v)

        # v에서 u로 가는 간선 추가
        self.adj[v].append(u)

        # 용량 저장
        self.cap[u][v] = c

        # 양방향일 경우 반대 간선의 용량도 저장
        self.cap[v][u] = 0 if d else c

    def dinic(self, s: int, t: int) -> int:
        """
        이 메소드는 Dinic의 알고리즘을 사용하여 최대 유량을 계산합니다.
        각 반복마다 BFS를 사용하여 증가 경로를 찾고, DFS를 사용하여 유량을 증가시킵니다.

        Args:
            s (int): 최대 유량의 시작 정점
            t (int): 최대 유량의 도착 정점

        Returns:
            int: s에서 t로의 최대 유량
        """

        # 최대 유량을 저장할 변수
        mf = 0

        # s에서 t로의 경로가 존재하는 동안 반복
        while self.bfs(s, t):

            # 각 노드의 마지막 방문한 간선 초기화
            self.last = [0 for _ in range(self.size)]

            # s에서 t로의 경로를 찾고, 해당 경로에서의 유량을 계산하여 f에 저장
            while f := self.dfs(s, t):

                # 최대 유량에 f(해당 경로의 유량)를 더함
                mf += f
        
        # 최대 유량 반환
        return mf

    def bfs(self, s: int, t: int) -> bool:
        """
        이 메소드는 BFS를 사용하여 최단 증가 경로를 찾습니다.
        증가 경로가 있는 경우 True를 반환하고, 없는 경우 False를 반환합니다.

        Args:
            s (int): 탐색의 시작 정점
            t (int): 탐색의 목표 정점

        Returns:
            bool: 증가 경로의 존재 여부
        """

        # 모든 노드의 거리를 -1로 초기화 ( 시작 노드의 거리는 0으로 설정 )
        self.depth = [-1 for _ in range(s)] + [0] + [-1 for _ in range(self.size - s - 1)]

        # 시작 정점으로 큐 초기화
        queue = deque([s])

        # 큐가 빌 때까지 반복
        while queue:

            # 큐에서 노드 하나를 꺼냄
            u = queue.popleft()

            # 해당 노드와 연결된 모든 노드에 대해 반복
            for v in self.adj[u]:

                # 도착 노드가 아직 방문되지 않았고 잔여 용량이 있는 경우 ( 흐름이 용량보다 작은 경우 )
                if self.depth[v] == -1 and self.flow[u][v] < self.cap[u][v]:

                    # 도착 노드의 거리를 업데이트
                    self.depth[v] = self.depth[u] + 1

                    # 큐에 추가
                    queue.append(v)

                    # 도착 노드에 도달한 경우
                    if v == t:
                        
                        # 증가 경로가 존잻람을 반환
                        return True
        
        # 증가 경로가 없음을 반환
        return False

    def dfs(self, u: int, t: int, f: int = float('inf')) -> int:
        """
        이 메소드는 DFS를 사용하여 유량을 증가시킵니다.
        잔여 용량이 있는 간선을 따라 증가 경로를 찾고 유량을 증가시킵니다.

        Args:
            u (int): 현재 정점
            t (int): 목표 정점
            f (int, optional): 가능한 최대 유량, 기본값은 INF

        Returns:
            int: 증가된 유량의 값
        """

        # 도착 노드에 도달한 경우
        if u == t:

            # 현재 경로에서의 유량을 반환
            return f
        
        # 노드 u의 모든 인접한 간선에 대해 반복
        while self.last[u] < len(self.adj[u]):

            # 다음으로 방문할 노드
            v = self.adj[u][self.last[u]]

            # 도착 노드가 최단 경로 상에 있고 잔여 용량이 있는 경우 ( 흐름이 용량보다 작은 경우 )
            if self.depth[v] == self.depth[u] + 1 and self.flow[u][v] < self.cap[u][v]:

                # 재귀적으로 경로를 찾고 유량을 계산
                pushed = self.dfs(v, t, min(f, self.cap[u][v] - self.flow[u][v]))

                # 유량을 보낼 수 있는 경우 ( 유량이 증가된 경우 )
                if pushed:

                    # 유량 추가
                    self.flow[u][v] += pushed

                    # 역방향 간선의 유량 제거
                    self.flow[v][u] -= pushed

                    # 증가된 유량 반환
                    return pushed
                
            # 다음 간선으로 이동
            self.last[u] += 1
        
        # 증가된 유량 없음
        return 0