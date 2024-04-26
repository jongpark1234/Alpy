import heapq

class Dijkstra:
    """Dijkstra 알고리즘을 활용한 최단 거리를 구하는 클래스입니다."""

    def process(self, graph: list[list[tuple]], start: int) -> list[int]:
        """
        process 함수는 Dijkstra 알고리즘을 사용하여 주어진 그래프에서 시작 노드로부터 각 노드까지의 최단 거리를 계산하는 메서드입니다.
        이 함수는 그래프와 시작 노드를 인자로 받아들이고, 시작 노드로부터 각 노드까지의 최단 거리를 담은 리스트를 반환합니다.

        알고리즘은 다음과 같이 작동합니다:

        1. 시작 노드의 최단 거리를 0으로 설정하고, 나머지 노드의 최단 거리를 무한대로 초기화합니다. 시작 노드를 힙에 추가합니다.
        2. 힙이 비어 있지 않은 동안 다음을 반복합니다:
                - 힙에서 최단 거리를 가지는 노드를 꺼냅니다.
                - 해당 노드와 연결된 모든 인접한 노드를 확인하고, 현재까지의 최단 거리보다 더 짧은 거리를 찾습니다.
                - 더 짧은 거리를 찾으면 해당 노드까지의 최단 거리를 갱신하고, 힙에 추가합니다.
        3. 모든 노드에 대한 최단 거리가 계산된 후, 최단 거리를 담은 리스트를 반환합니다.

        이 알고리즘은 각 노드를 한 번씩만 방문하며, 그래프의 엣지를 최대한 적게 탐색하여 효율적으로 최단 거리를 계산합니다.

        Args:
            graph (list[list[tuple]]): 최단 거리를 계산할 그래프를 나타내는 인접 리스트입니다.
            각 노드에 대한 인접한 노드들과 가중치의 리스트로 구성됩니다.
            예를 들어, graph[i]는 노드 i와 인접한 노드들과 그에 상응하는 가중치들의 리스트입니다.

            start (int): 최단 거리 계산의 시작점이 되는 노드의 인덱스입니다.

        Returns:
            list[int]: 시작 노드로부터 각 노드까지의 최단 거리를 담은 리스트입니다. dist[i]는 시작 노드로부터 노드 i까지의 최단 거리를 나타냅니다.
        """

        # 탐색할 노드를 저장할 최소 힙
        heap = [(0, start)]
        heapq.heapify(heap)

        # start 노드에서 각각의 노드로 가기까지 필요한 거리를 저장할 리스트
        dist = [float('inf') for _ in range(len(graph))]
        dist[start] = 0

        # 탐색을 완료할 때까지 반복
        while heap:

            # 현재 탐색할 노드와 현재까지의 가중치 합
            cur_cost, cur_node = heapq.heappop(heap)

            # 이미 해당 노드에 다른 더 빠른 경로로 올 수 있을 경우 탐색하지 않음
            if cur_cost > dist[cur_node]:
                continue

            # 현재 탐색하는 노드와 인접한 노드 탐색
            for next_cost, next_node in graph[cur_node]:

                # 현재까지의 가중치 합에 새 노드로 이동할 때 소모되는 가중치 추가
                next_cost += cur_cost

                # 이미 다음 노드에 다른 더 빠른 경로로 갈 수 있을 경우 탐색하지 않음
                if next_cost > dist[next_node]:
                    continue

                # 다음 노드까지 소모되는 최단 거리 가중치 갱신
                dist[next_node] = next_cost

                # 다음 노드를 힙에 넣어 계속해서 탐색
                heapq.heappush(heap, (next_cost, next_node))

        # start 노드부터 각각의 노드에 가기까지 소모되는 최소 가중치 리스트를 반환
        return dist