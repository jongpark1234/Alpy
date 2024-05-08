from collections import deque

class MCMF:
    """
    최소 비용 최대 유량(Minimum Cost Maximum Flow, MCMF) 알고리즘을 SPFA를 이용하여 구현한 클래스입니다.
    """

    def __init__(self, v: int):

        # v개의 정점을 가진 유량 그래프 초기화
        self.size = v

        # 그래프의 인접 리스트
        self.adj = [[] for _ in range(v)]

        # 용량을 저장하는 인접 리스트
        self.cap = [[0 for _ in range(v)] for _ in range(v)]

        # 흐름을 저장하는 인접 리스트
        self.flow = [[0 for _ in range(v)] for _ in range(v)]

        # 비용을 저장하는 인접 리스트
        self.cost = [[0 for _ in range(v)] for _ in range(v)]

        # 각 노드까지의 거리를 저장하는 리스트
        self.depth = [0 for _ in range(v)]

        # 각 노드의 마지막으로 방문한 간선을 저장하는 리스트
        self.last = [0 for _ in range(v)]

        # 각 노드의 방문 여부를 저장하는 리스트
        self.visited = [False for _ in range(v)]

        # 총 비용
        self.total_cost = 0

    def add_edge(self, u: int, v: int, w: int, c: float, d: bool=True):
        """
        u에서 v로 가는 간선과 v에서 u로 가는 역방향 간선을 추가합니다.
        양방향 간선이 아닌 경우, 역방향 간선도 추가됩니다.
        
        Args:
            u (int): 출발 정점
            v (int): 도착 정점
            w (int): 간선의 용량
            c (float): 간선의 비용
            d (bool, optional): 양방향 간선인지의 여부
        """

        # u에서 v로 가는 간선 추가
        self.adj[u].append(v)

        # v에서 u로 가는 간선 추가
        self.adj[v].append(u)

        # 용량 저장
        self.cap[u][v] = w

        # 비용 저장
        self.cost[u][v] = c

        # 역방향 간선의 비용 저장
        self.cost[v][u] = -c

        # 양방향 간선이 아닌 경우
        if not d:

            # 역방향 간선 추가
            self.add_edge(v, u, w, c)

    def mcmf(self, s: int, t: int) -> tuple[int, float]:
        """
        최소 비용 최대 유량(Minimum Cost Maximum Flow, MCMF) 알고리즘을 수행하는 함수입니다.

        시작 정점에서 도착 정점까지의 최단 경로가 존재하는 동안 반복합니다.

        시작 정점에서 도착 정점까지의 경로를 찾고 유량을 계산합니다.

        최대 유량과 최소 비용을 반환합니다.
        
        Args:
            s (int): 시작 정점
            t (int): 도착 정점
        
        Returns:
            tuple[int, float]: 최대 유량과 최소 비용을 담은 튜플
        """

        # 최대 유량, 최소 비용
        mf = mc = 0

        # 시작 노드에서 도착 노드까지의 최단 경로가 존재하는 동안 반복
        while self.spfa(s, t):

            # 마지막 방문한 간선 배열 초기화
            self.last = [0 for _ in range(self.size)]

            # 시작 노드에서 도착 노드까지의 경로를 찾고 유량을 계산하여 f에 저장
            while f := self.dfs(s, t):

                # 최대 유량 업데이트
                mf += f

                # 총 비용 업데이트
                mc += self.total_cost

                # 총 비용 초기화
                self.total_cost = 0

        # 최대 유량과 최소 비용 반환
        return mf, mc

    def spfa(self, s: int, t: int) -> bool:
        """
        Shortest Path Faster Algorithm (SPFA)을 수행하여 시작 정점부터 도착 정점까지의 최단 경로가 존재하는지 확인하는 함수입니다.
        
        시작 정점부터 도착 정점까지의 최단 경로가 존재하는지 확인합니다. 최단 경로가 존재한다면 True를 반환하고, 그렇지 않다면 False를 반환합니다.
        
        Args:
            s (int): 시작 정점
            t (int): 도착 정점
        
        Returns:
            bool: 시작 정점부터 도착 정점까지의 최단 경로가 존재하는지 여부
        """

        # 모든 노드의 거리를 무한대로 초기화
        self.depth = [float('inf') for _ in range(s)] + [0] + [float('inf') for _ in range(self.size - s - 1)]

        # 시작 노드를 방문 표시
        self.visited[s] = True

        # 큐 생성
        queue = deque([s])

        # 큐가 빌 때까지 반복
        while queue:

            # 큐에서 노드 하나를 꺼냄
            u = queue.popleft()

            # 해당 노드를 방문하지 않았음으로 표시
            self.visited[u] = False

            # 해당 노드와 연결된 모든 간선에 대해 반복
            for v in self.adj[u]:

                # 잔여 용량이 있으며, v로 이동하는 것이 경로의 비용을 더 줄일 수 있는 경우
                if self.flow[u][v] < self.cap[u][v] and self.depth[v] > self.depth[u] + self.cost[u][v]:

                    # 거리 업데이트
                    self.depth[v] = self.depth[u] + self.cost[u][v]

                    # 해당 노드를 방문하지 않은 경우
                    if not self.visited[v]:

                        # 방문 표시
                        self.visited[v] = True

                        # 큐에 추가
                        queue.append(v)

        # 도착 노드까지의 최단 경로가 존재하는지 여부 반환
        return self.depth[t] < float('inf')

    def dfs(self, u: int, t: int, f: int=float('inf')) -> int:
        """
        Depth First Search (DFS)를 이용하여 시작 정점부터 도착 정점까지의 경로를 찾고 유량을 계산하는 함수입니다.
        
        Args:
            u (int): 현재 정점
            t (int): 도착 정점
            f (int, optional): 현재 경로에서의 최대 유량
        
        Returns:
            int: 현재 경로에서의 유량
        """

        # 도착 노드에 도달한 경우
        if u == t:

            # 현재 경로에서의 유량을 반환
            return f
        
        # 해당 노드를 방문했음을 표시
        self.visited[u] = True

        # 해당 노드의 모든 인접한 간선에 대해 반복
        for v in self.adj[u][self.last[u]:len(self.adj[u])]:

            # 노드 v가 아직 방문되지 않았고, 잔여 용량이 있으며, v로 이동하는 것이 현재까지의 최단 경로의 비용을 유지할 수 있는 경우
            if not self.visited[v] and self.flow[u][v] < self.cap[u][v] and self.depth[v] == self.depth[u] + self.cost[u][v]:

                # 재귀적으로 경로를 찾고 유량을 계산
                pushed = self.dfs(v, t, min(f, self.cap[u][v] - self.flow[u][v]))

                # 유량을 보낼 수 있는 경우
                if pushed:
                    
                    # 총 비용 업데이트
                    self.total_cost += pushed * self.cost[u][v]

                    # 유량 추가
                    self.flow[u][v] += pushed

                    # 역방향 간선의 유량 제거
                    self.flow[v][u] -= pushed

                    # 해당 노드를 방문하지 않은 상태로 변경
                    self.visited[u] = False

                    # 유량 반환
                    return pushed
                
        # 해당 노드를 방문하지 않은 상태로 변경
        self.visited[u] = False

        # 유량이 없음을 나타내는 0 반환
        return 0
