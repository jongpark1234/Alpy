class SCC:
    """
    이 클래스는 Kosaraju 알고리즘을 사용하여
    주어진 그래프의 강한 연결 요소 (Strongly Connected Component, SCC)를 찾는 데 사용되는 클래스입니다.
    """

    @staticmethod
    def strongly_connected_component(graph: list[list[int]]) -> tuple[list[list[int]], list[int]]:
        """
        그래프를 인자로 받아 해당 그래프의 강한 연결 요소들을 찾는 메소드입니다.

        Args:
            graph (list[list[int]]): 그래프를 인접 리스트로 표현한 것입니다. 각 노드에 대해 연결된 노드들의 리스트가 포함됩니다.

        Returns:
            tuple: (강한 연결 요소들의 리스트, 노드별 SCC 번호를 저장한 리스트)의 튜플을 반환합니다.
        """

        # 그래프의 크기
        size = len(graph)

        # SCC 정보를 저장할 리스트
        scc = []

        # 각 노드의 SCC 번호를 저장할 리스트
        scc_by_node = [None for _ in range(size)]

        # 각 노드의 깊이를 저장할 리스트
        depth = [0 for _ in range(size)]

        # s: 방문한 노드들의 경로 저장, p: 각 노드의 깊이 저장
        path, p = [], []
        
        # 스택 ( [ 0, 1, ..., s-2, s-1 ] )
        while (stack := list(range(size))):

            # 스택에서 노드를 꺼냄
            u = stack.pop()

            # 꺼낸 노드가 음수라면 현재 역방향으로 탐색중이라는 의미
            if u < 0:

                # 현재 노드의 깊이
                d = depth[~u] - 1
                
                # 현재 깊이가 p 배열의 가장 위의 값보다 작다면 현재 노드와 연결된 SCC를 찾은것
                if p[-1] > d:
                    
                    # SCC 번호 할당
                    scc_no = len(scc)

                    # SCC 리스트에 현재 노드부터 끝까지의 경로를 추가
                    scc.append(path[d:])

                    # s, p 배열에서 이전 경로의 정보 제거
                    del path[d:], p[-1]

                    # SCC에 속한 노드들의 SCC 번호 할당
                    for v in scc[-1]:
                        scc_by_node[v] = scc_no

            # 현재 노드가 아직 SCC에 할당되지 않은 경우
            elif scc_by_node[u] is None:

                # 노드 깊이 확인 및 이미 방문한 노드인지 확인
                if (d := depth[u]) > 0:

                    # 이전에 방문한 노드의 깊이보다 더 깊은 높이를 갖는 노드는 스택에서 제거
                    while p[-1] > d:
                        p.pop()

                # 새로운 노드 탐색
                else:
                    path.append(u)
                    p.append(len(path))
                    depth[u] = len(path)
                    stack.append(~u)
                    stack.extend(graph[u])
        
        # SCC 리스트 및 각 노드의 SCC 정보 반환
        return scc, scc_by_node