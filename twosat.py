from scc import SCC
from itertools import permutations, pairwise

class TwoSat:
    '''2-SAT solver.'''

    def __init__(self, var_count: int) -> None:
        """
        TwoSat 클래스의 초기화 메소드입니다.

        Args:
            var_count (int): 변수의 개수를 나타내는 정수입니다.
        """
        self._graph = [set() for _ in range(var_count * 2)]
        self._var_ord = self._neg_var_ord = None
    
    def _mapping(self, x: int) -> int:
        """
        해당 구문은 주어진 변수 x에 대해 참임을 나타내는 정점을 그래프에 추가하기 전에 변수의 인덱스를 적절히 매핑하는 과정을 수행합니다.
        
        구문을 자세히 설명하면 다음과 같습니다:

        x가 음수인 경우:
            음수 변수에 대해서는 부정을 나타내는 정점을 생성해야 합니다. 따라서 음수 변수에 대해 해당 변수를 양수로 바꾼 뒤, 부정 연산을 수행합니다.
            
            x가 음수인 경우, x + x를 계산하면 양수 값이 됩니다.
            
            부정 연산을 위해 -1 - x - x를 수행합니다. 이것은 x의 부정 값을 의미합니다.

        x가 양수인 경우:
            양수 변수는 해당 변수를 그대로 사용합니다.

            x가 양수인 경우, x + x를 계산하면 2를 곱한 값이 됩니다. 따라서 이 경우에는 변수를 그대로 사용합니다.
        
        Args:
            x (int): 특정 변수의 인덱스입니다.
        
        Returns:
            int: 매핑된 그래프의 인덱스를 반환합니다.
        """

        return x + x if x >= 0 else -1 - x - x


    def x_is_true(self, x: int) -> None:
        """
        x 변수가 참임을 나타내는 절을 그래프에 추가하는 메소드입니다.

        Args:
            x (int): 참임을 나타내는 변수의 인덱스입니다.
        """

        # 변수의 인덱스를 그래프 상의 정점으로 매핑
        x = self._mapping(x)

        # x 변수가 참일 때, 그래프에 해당 변수의 부정을 나타내는 정점 추가
        self._graph[x ^ 1].add(x)

    def x_or_y(self, x: int, y: int) -> None:
        """
        x 또는 y 중 적어도 하나가 참임을 나타내는 절을 그래프에 추가하는 메소드입니다.

        Args:
            x (int): 첫 번째 변수의 인덱스입니다.
            y (int): 두 번째 변수의 인덱스입니다.
        """

        # x와 y를 매핑하여 그래프 상의 정점으로 변환
        x = self._mapping(x)
        y = self._mapping(y)
        
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

        # x와 y를 매핑하여 그래프 상의 정점으로 변환
        x = self._mapping(x)
        y = self._mapping(y)

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

        # 변수들을 그래프 상의 정점으로 매핑
        x = [self._mapping(i) for i in x]

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
            self._graph[y0 + 1] = (x[0] ^ 1,)
            self._graph[y_i - 2] = (x[-1] ^ 1)

    def is_satisfiable(self) -> bool:
        """
        2-SAT 문제의 충족 가능성 여부를 반환하는 메소드입니다.

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
        """
        충족 가능한 경우 참 값의 할당을 찾는 메소드입니다.

        Returns:
            list[bool]: 충족 가능한 경우 변수에 대한 참 값의 할당을 나타내는 리스트입니다.
        """
        
        # 문제가 충족 불가능하다면 ValueError를 Raise
        if not self.is_satisfiable():
            raise ValueError('No truth assignment exists.')
        
        # 충족 가능한 경우, 변수에 대한 참 값의 할당을 생성하여 반환
        # 각 변수와 그 부정 변수의 순서를 비교하여 참 값의 할당을 결정
        return [x < y for x, y in zip(self._var_ord, self._neg_var_ord)]