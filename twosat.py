from scc import SCC
from itertools import permutations, pairwise

class TwoSat:
    '''2-SAT solver.'''

    __slot__ = ('_n', '_graph', '_ord', '_nord')

    def __init__(self, var_count: int) -> None:
        self._n = var_count
        self._graph = [set() for _ in range(var_count * 2)]
        self._ord = self._nord = None

    def x_is_true(self, x: int) -> None:
        x = x + x if x >= 0 else -1 - x - x
        self._graph[x ^ 1].add(x)

    def x_or_y(self, x: int, y: int) -> None:
        x = x + x if x >= 0 else -1 - x - x
        y = y + y if y >= 0 else -1 - y - y
        self._graph[x ^ 1].add(y)
        self._graph[y ^ 1].add(x)

    def x_eq_y(self, x: int, y: int) -> None:
        x = x + x if x >= 0 else -1 - x - x
        y = y + y if y >= 0 else -1 - y - y
        self._graph[x].add(y)
        self._graph[x ^ 1].add(y ^ 1)
        self._graph[y].add(x)
        self._graph[y ^ 1].add(x ^ 1)

    def at_most_one(self, x: list[int]) -> None:
        x = [x_i + x_i if x_i >= 0 else -1 - x_i - x_i for x_i in x]
        if len(x) <= 4:
            for x_i, x_j in permutations(x, 2):
                self._graph[x_i].add(x_j ^ 1)
        else:
            y_i = y0 = len(self._graph)
            for x0, x1 in pairwise(x):
                self._graph.append((y_i + 2, x1 ^ 1))
                self._graph.append((y_i - 1, x0 ^ 1))
                self._graph[x0].add(y_i)
                self._graph[x1].add(y_i + 1)
                y_i += 2
            self._graph[y0 + 1] = (x[0] ^ 1,)
            self._graph[y_i - 2] = (x[-1] ^ 1,)

    def is_satisfiable(self) -> bool:
        """
        문제의 충족 가능성 여부를 반환하는 메소드입니다.

        Returns:
            bool: 문제가 충족 가능하면 True, 아니면 False를 반환합니다.
        """

        if self._var_ord is None:

            # 그래프의 강한 연결 요소 구해오기
            _, scc_no = SCC.strongly_connected_component(self._graph)

            # 각 변수의 순서와 부정 변수의 순서 분리
            self._var_ord, self._neg_var_ord = scc_no[::2], scc_no[1::2]

        # 모든 변수와 그 부정 변수가 같지 않은지 확인하여 충족 가능성 여부 반환
        return all(x != y for x, y in zip(self._var_ord, self._neg_var_ord))

    def find_truth_assignment(self) -> list[bool]:
        if not self.is_satisfiable():
            raise ValueError('No truth assignment exists.')
        return [x < y for x, y in zip(self._var_ord, self._neg_var_ord)]