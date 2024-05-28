from scc import SCC
from itertools import permutations, pairwise

class TwoSat:
    """2-SAT solver."""

    def __init__(self, var_count: int) -> None:
        """
        TwoSat 클래스의 초기화 메소드입니다.

        Args:
            var_count (int): 변수의 개수를 나타내는 정수입니다.
        """
        self.n = var_count
        self._graph = [set() for _ in range(var_count * 2)]
        self._ord = self._nord = None

    def x_is_true(self, x: int) -> None:
        """
        x 변수가 참임을 나타내는 절을 그래프에 추가하는 메소드입니다.

        Args:
            x (int): 참임을 나타내는 변수의 인덱스입니다.
        """

        # x 변수가 참일 때, 그래프에 해당 변수의 부정을 나타내는 정점 추가
        self._graph[x ^ 1].add(x)

    def x_or_y(self, x: int, y: int) -> None:
        """
        x 또는 y 중 적어도 하나가 참임을 나타내는 절을 그래프에 추가하는 메소드입니다.

        Args:
            x (int): 첫 번째 변수의 인덱스입니다.
            y (int): 두 번째 변수의 인덱스입니다.
        """
        
        # x 또는 y 중 적어도 하나가 참일 때, 서로의 부정을 나타내는 정점 추가
        self._graph[x ^ 1].add(y)
        self._graph[y ^ 1].add(x)

    def x_eq_y(self, x: int, y: int) -> None:
        """
        x와 y가 동시에 참이거나 동시에 거짓임을 나타내는 절을 그래프에 추가하는 메소드입니다.

        Args:
            x (int): 첫 번째 변수의 인덱스입니다.
            y (int): 두 번째 변수의 인덱스입니다.
        """

         # x와 y가 동시에 참이거나 동시에 거짓일 때, 해당 관계를 나타내는 간선 추가
        self._graph[x].add(y)
        self._graph[x ^ 1].add(y ^ 1)
        self._graph[y].add(x)
        self._graph[y ^ 1].add(x ^ 1)

    def at_most_one(self, x: list[int]) -> None:
        """
        주어진 변수들 중 최대 하나만 참이 될 수 있는 절을 그래프에 추가하는 메소드입니다.

        Args:
            x (list[int]): 변수들의 인덱스로 이루어진 리스트입니다.
        """

        # 변수의 개수가 4 이하인 경우 모든 변수 쌍에 대해 서로 부정을 나타내는 간선 추가
        if len(x) <= 4:
            for i, j in permutations(x, 2):
                self._graph[i].add(j ^ 1)

        # 변수의 개수가 4보다 큰 경우 새로운 정점을 추가하고 해당 변수들의 관계를 나타내는 간선 추가
        else:
            y_i = y0 = len(self._graph)
            for x0, x1 in pairwise(x):
                self._graph.append((y_i + 2, x1 ^ 1))
                self._graph.append((y_i - 1, x0 ^ 1))
                self._graph[x0].add(y_i)
                self._graph[x1].add(y_i + 1)
                y_i += 2
            
            # 첫 번째 변수와 마지막 변수의 관계를 나타내는 간선 추가
            self._graph[y0 + 1] = x[0] ^ 1
            self._graph[y_i - 2] = x[-1] ^ 1

    def is_satisfiable(self) -> bool:
        """
        2-SAT 문제의 충족 가능성 여부를 반환하는 메소드입니다.

        Returns:
            bool: 문제가 충족 가능하면 True, 아니면 False를 반환합니다.
        """

        if self._ord is None:

            # 그래프의 강한 연결 요소 구해오기
            _, scc_no = SCC.strongly_connected_component(self._graph)

            # 각 변수의 순서와 부정 변수의 순서 분리
            self._ord, self._nord = scc_no[::2], scc_no[1::2]

        # 모든 변수와 그 부정 변수가 같지 않은지 확인하여 충족 가능성 여부 반환
        return all(x != y for x, y in zip(self._ord, self._nord))

    def find_truth_assignment(self) -> list[bool]:
        """
        충족 가능한 경우 참 값의 할당을 찾는 메소드입니다.

        Returns:
            list[bool]: 충족 가능한 경우 변수에 대한 참 값의 할당을 나타내는 리스트입니다.
        """
        
        # 문제가 충족 불가능하다면 None을 반환
        if not self.is_satisfiable():
            return None
        
        # 충족 가능한 경우, 변수에 대한 참 값의 할당을 생성하여 반환
        # 각 변수와 그 부정 변수의 순서를 비교하여 참 값의 할당을 결정
        return [x < y for x, y, _ in zip(self._ord, self._nord, range(self.n))]