from collections import deque
class MF:
    """
    이 클래스는 최대 유량 문제를 해결하기 위한 Dinic 알고리즘을 구현한 것입니다.

    최대 유량 문제는 네트워크의 각 간선에 용량이 할당되어 있고,
    한 정점에서 다른 정점으로 유량을 흘려보내는 과정에서 최대로 보낼 수 있는 유량을 찾는 문제입니다.

    이 클래스는 그래프의 구조를 나타내는 인접 리스트를 사용하여 그래프를 표현하고,
    Dinic 알고리즘을 이용하여 최대 유량을 계산합니다.
    """
    
    def __init__(self, v: int):
        # v개의 정점을 가진 최대 유량 그래프 초기화
        self.size = v

        # 그래프의 인접 리스트
        self.adj = [[] for _ in range(v)]

        # BFS에 사용되는 깊이 배열
        self.depth = [0 for _ in range(v)]

        # DFS에서 마지막 방문한 간선을 저장하는 배열
        self.last = [0 for _ in range(v)]

        # 간선을 저장하는 리스트
        self.edges = []

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

        # edge에서의 간선 인덱스 추가
        self.adj[u].append(len(self.edges))

        # 원래 간선 추가
        self.edges.append((v, c, 0))

        # edge에서의 간선 인덱스 추가
        self.adj[v].append(len(self.edges))

        # 양방향일 경우 반대 간선 추가
        self.edges.append((u, 0 if d else c, 0))

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

        # 최대 유량 초기화
        mf = 0

        # 증가 경로가 존재하는 동안
        while self.bfs(s, t):

            # 마지막으로 방문한 간선 배열 초기화
            self.last = [0 for _ in range(self.size)]

            # s에서 t로의 유량 증가 경로가 있는 동안
            while f := self.dfs(s, t):

                # 유량을 최대 유량에 추가
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

        # 깊이 배열 초기화
        self.depth = [-1 for _ in range(s)] + [0] + [-1 for _ in range(self.adj - s - 1)]

        # 출발 정점으로 큐 초기화
        queue = deque([s])

        # 큐가 비어있지 않은 동안
        while queue:

            # 큐에서 정점 추출
            u = queue.popleft()

            # 정점과 연결된 간선들에 대해 반복
            for idx in self.adj[u]:

                # 도착 정점, 용량, 유량
                v, cap, flow = self.edges[idx]

                # 도착 정점이 방문되지 않았고 잔여 용량이 있는 경우
                if self.depth[v] == -1 and flow < cap:

                    # 도착 정점의 거리 설정
                    self.depth[v] = self.depth[u] + 1

                    # 도착 정점을 큐에 추가
                    queue.append(v)

                    # 도착 정점이 싱크 정점인 경우
                    if v == t:
                        
                        # 증가 경로 발견
                        return True
        
        # 증가 경로 없음
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

        # 현재 정점이 싱크 정점인 경우
        if u == t:

            # 유량 반환
            return f
        
        # 방문되지 않은 이웃이 있는 경우
        while self.last[u] < len(self.adj[u]):

            # 간선 인덱스 얻기
            idx = self.adj[u][self.last[u]]

            # 도착 정점, 용량, 유량 얻기
            v, cap, flow = self.edges[idx]

            # 도착 정점이 최단 경로 상에 있고 잔여 용량이 있는 경우
            if self.depth[v] == self.depth[u] + 1 and flow < cap:

                # 재귀적으로 유량 증가 찾기
                pushed = self.dfs(v, t, min(f, cap - flow))

                # 유량이 증가된 경우
                if pushed:

                    # 정방향 간선 업데이트
                    self.edges[idx] = (v, cap, flow + pushed)

                    # 역방향 간선 업데이트
                    self.edges[idx ^ 1] = (self.edges[idx ^ 1][0], self.edges[idx ^ 1][1], self.edges[idx ^ 1][2] - pushed)

                    # 증가된 유량 반환
                    return pushed
                
            # 다음 간선으로 이동
            self.last[u] += 1
        
        # 증가된 유량 없음
        return 0