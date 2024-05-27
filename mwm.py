from heapq import heappush, heappop
from itertools import accumulate
from collections import deque
from sys import stdin
from math import inf

class EdgeEvent:
    def __init__(self, time: int, frm: int, to: int):
        """
        간선 이벤트 객체를 초기화합니다.

        Args:
            time (int): 이벤트 발생 시간
            frm (int): 간선의 시작 정점
            to (int): 간선의 끝 정점
        """

        # 이벤트 발생 시간
        self.time = time

        # 간선의 시작 정점
        self.frm = frm

        # 간선의 끝 정점
        self.to = to
    
    def __lt__(self, rhs: 'EdgeEvent') -> bool:
        """
        두 간선 이벤트 객체를 비교합니다. 시간 기준으로 비교합니다.

        Args:
            rhs (EdgeEvent): 비교할 다른 간선 이벤트 객체

        Returns:
            bool: 현재 객체의 시간이 더 작으면 True, 그렇지 않으면 False
        """
        return self.time < rhs.time
    
    def __gt__(self, rhs: 'EdgeEvent') -> bool:
        """
        두 간선 이벤트 객체를 비교합니다. 시간 기준으로 비교합니다.

        Args:
            rhs (EdgeEvent): 비교할 다른 간선 이벤트 객체

        Returns:
            bool: 현재 객체의 시간이 더 크면 True, 그렇지 않으면 False
        """
        return self.time > rhs.time

class BinaryHeap:
    class Node:
        def __init__(self, value: int | EdgeEvent, id: int = 0):
            """
            힙 노드를 초기화합니다.

            Args:
                value (int | EdgeEvent): 노드의 값
                id (int, optional): 노드의 ID.
            """

            # 노드의 값
            self.value = value

            # 노드의 ID
            self.id = id

        def __lt__(self, rhs: 'BinaryHeap.Node') -> bool:
            """
            노드의 값을 비교합니다.

            Args:
                rhs (BinaryHeap.Node): 비교할 노드

            Returns:
                bool: 현재 노드의 값이 rhs 노드의 값보다 작은지 여부
            """
            return self.value < rhs.value

    def __init__(self, n: int, isEdgeEvent: bool):
        """
        이진 힙을 초기화합니다.

        Args:
            n (int): 힙에 저장할 수 있는 최대 노드 수
            isEdgeEvent (bool): 노드 값의 타입이 EdgeEvent인지 여부
        """

        # 현재 힙의 크기
        self.size_ = 0

        # 노드 배열
        self.node = [BinaryHeap.Node(EdgeEvent(0, 0, 0) if isEdgeEvent else 0) for _ in range(n + 1)]

        # 인덱스 배열
        self.index = [0 for _ in range(n)]

    def size(self) -> int:
        """
        힙의 크기를 반환합니다.

        Returns:
            int: 힙의 크기
        """
        return self.size_

    def empty(self) -> bool:
        """
        힙이 비어 있는지 확인합니다.

        Returns:
            bool: 힙이 비어 있으면 True, 아니면 False
        """
        return self.size_ == 0

    def clear(self) -> None:
        """
        힙을 초기화합니다.
        """

        # 힙에 원소가 존재하지 않을 때까지 반복
        while self.size_ > 0:

            # 해당 인덱스를 0으로 설정
            self.index[self.node[self.size_].id] = 0

            # 힙 크기를 감소
            self.size_ -= 1

    def min(self) -> int | EdgeEvent:
        """
        힙에서 최소 값을 반환합니다.

        Returns:
            int | EdgeEvent: 힙의 최소 값
        """
        return self.node[1].value

    def argmin(self) -> int:
        """
        힙에서 최소 값의 ID를 반환합니다.

        Returns:
            int: 최소 값의 ID
        """
        return self.node[1].id

    def get_val(self, id: int) -> int | EdgeEvent:
        """
        주어진 ID의 값을 반환합니다.

        Args:
            id (int): 값을 가져올 노드의 ID

        Returns:
            int | EdgeEvent: 노드의 값
        """
        return self.node[self.index[id]].value

    def pop(self) -> None:
        """
        힙에서 최소 값을 제거합니다.
        """

        # 힙이 비어있지 않은 경우 루트 노드를 제거
        if self.size_ > 0:
            self._pop(1)

    def erase(self, id: int) -> None:
        """
        주어진 ID의 노드를 힙에서 제거합니다.

        Args:
            id (int): 제거할 노드의 ID
        """

        # 주어진 ID의 노드가 존재한다면 해당 노드를 제거
        if self.index[id]:
            self._pop(self.index[id])

    def has(self, id: int) -> bool:
        """
        주어진 ID의 노드가 힙에 존재하는지 확인합니다.

        Args:
            id (int): 확인할 노드의 ID

        Returns:
            bool: 노드가 존재하면 True, 아니면 False
        """
        return self.index[id] != 0

    def update(self, id: int, v: int | EdgeEvent) -> None:
        """
        주어진 ID의 노드 값을 갱신합니다.

        Args:
            id (int): 갱신할 노드의 ID
            v (int | EdgeEvent): 새로운 값
        """

        # 노드가 없으면 힙에 추가
        if not self.has(id):
            self.push(id, v)
            return
        
        # 새로운 값이 더 작은지 여부
        up = v < self.node[self.index[id]].value

        # 노드 값을 갱신
        self.node[self.index[id]].value = v

        # 새로운 값이 더 작은 경우 값을 위로 올림
        if up:
            self._up_heap(self.index[id])

        # 새로운 값이 더 큰 경우 값을 아래로 내림
        else:
            self._down_heap(self.index[id])

    def decrease_key(self, id: int, v: int | EdgeEvent) -> None:
        """
        주어진 ID의 노드 값을 감소시킵니다.

        Args:
            id (int): 갱신할 노드의 ID
            v (int | EdgeEvent): 새로운 값
        """

        # 노드가 없으면 힙에 추가
        if not self.has(id):
            self.push(id, v)
            return
        
        # 새로운 값이 더 작은 경우
        if v < self.node[self.index[id]].value:

            # 노드 값을 갱신
            self.node[self.index[id]].value = v

            # 값을 위로 올림
            self._up_heap(self.index[id])

    def push(self, id: int, v: int | EdgeEvent) -> None:
        """
        힙에 새로운 노드를 추가합니다.

        Args:
            id (int): 추가할 노드의 ID
            v (int | EdgeEvent): 추가할 값
        """

        # 힙 크기 증가
        self.size_ += 1

        # 인덱스 설정
        self.index[id] = self.size_

        # 노드 추가
        self.node[self.size_] = BinaryHeap.Node(v, id)

        # 값을 위로 올림
        self._up_heap(self.size_)

    def _pop(self, pos: int) -> None:
        """
        힙에서 주어진 위치의 노드를 제거합니다.

        Args:
            pos (int): 제거할 노드의 위치
        """

        # 인덱스를 0으로 설정
        self.index[self.node[pos].id] = 0

        # 제거할 노드의 위치가 힙 크기와 동일하다면
        if pos == self.size_:

            # 힙 크기 감소
            self.size_ -= 1
            return
        
        # 마지막 노드가 더 작은지 여부 확인
        up = self.node[self.size_].value < self.node[pos].value

        # 마지막 노드를 현재 위치로 이동
        self.node[pos] = self.node[self.size_]

        # 힙 크기 감소
        self.size_ -= 1

        # 인덱스 갱신
        self.index[self.node[pos].id] = pos

        # 마지막 노드가 더 작은 경우 값을 위로 올림
        if up:
            self._up_heap(pos)
        
        # 마지막 노드가 더 큰 경우 값을 아래로 내림
        else:
            self._down_heap(pos)

    def _swap_node(self, a: int, b: int):
        """
        주어진 두 위치의 노드를 교환합니다.

        Args:
            a (int): 첫 번째 노드의 위치
            b (int): 두 번째 노드의 위치
        """

        # 노드 교환
        self.node[a], self.node[b] = self.node[b], self.node[a]

        # 인덱스 갱신
        self.index[self.node[a].id] = a
        self.index[self.node[b].id] = b

    def _down_heap(self, pos: int):
        """
        힙을 아래로 이동하여 재정렬합니다.

        Args:
            pos (int): 재정렬할 노드의 위치
        """

        k = nk = pos
        while k << 1 <= self.size_:

            # 왼쪽 자식 노드와 비교하여 더 작은 값을 nk에 설정
            if self.node[k << 1] < self.node[nk]:
                nk = k << 1

            # 오른쪽 자식 노드와 비교하여 더 작은 값을 nk에 설정
            if (k << 1) + 1 <= self.size_ and self.node[(k << 1) + 1] < self.node[nk]:
                nk = (k << 1) + 1

            # k와 nk가 같으면 반복 종료
            if k == nk:
                break

            # 노드를 교환
            self._swap_node(k, nk)

            # k를 nk로 갱신
            k = nk

    def _up_heap(self, pos: int):
        """
        힙을 위로 이동하여 재정렬합니다.

        Args:
            pos (int): 재정렬할 노드의 위치
        """
        k = pos
        while k > 1 and self.node[k] < self.node[k >> 1]:

            # 부모 노드와 비교하여 더 작은 값을 가진 노드로 교환
            self._swap_node(k, k >> 1)

            # k를 부모 노드로 갱신
            k >>= 1

class PairingHeaps:
    """
    페어링 힙(Pairing Heap)을 구현하는 클래스입니다.
    이 클래스는 힙을 여러 개의 트리 구조로 관리하여 효율적인 삽입, 삭제, 감소 키 연산을 지원합니다.
    """

    class Node:
        """
        페어링 힙의 노드를 나타내는 클래스입니다.
        """

        def __init__(self, key: EdgeEvent = EdgeEvent(0, 0, 0)):
        
            # 노드의 키 값 설정
            self.key = key

            # 자식 노드 초기화
            self.child = 0

            # 형제 노드 초기화
            self.next = 0

            # 루트 노드는 prev를 -1로 설정
            self.prev = -1 if key.time == key.frm == key.to == 0 else 0

    def __init__(self, h: int, n: int):

        # 루트 노드들을 저장할 리스트 초기화
        self.heap = [0 for _ in range(h)]

        # 노드들을 저장할 리스트 초기화
        self.node = [PairingHeaps.Node() for _ in range(n)]

    def clear(self, h: int) -> None:
        """
        특정 힙을 비웁니다.
        
        Args:
            h (int): 비우고자 하는 힙의 인덱스
        """

        # 재귀적으로 힙을 비움
        if self.heap[h]:
            self._clear_rec(self.heap[h])
            self.heap[h] = 0

    def clear_all(self) -> None:
        """
        모든 힙을 초기화하여 비웁니다.
        """

        # 모든 힙의 루트 노드들을 초기화
        for i in range(len(self.heap)):
            self.heap[i] = 0

        # 모든 노드들을 초기화
        for i in range(len(self.node)):
            self.node[i] = self.Node()

    def empty(self, h: int) -> bool:
        """
        특정 힙이 비어 있는지 확인합니다.
        
        Args:
            h (int): 확인하고자 하는 힙의 인덱스
        
        Returns:
            bool: 힙이 비어 있으면 True, 그렇지 않으면 False
        """
        return not self.heap[h]

    def used(self, v: int) -> bool:
        """
        특정 노드가 사용 중인지 확인합니다.
        
        Args:
            v (int): 확인하고자 하는 노드의 인덱스
        
        Returns:
            bool: 노드가 사용 중이면 True, 그렇지 않으면 False
        """
        return self.node[v].prev >= 0

    def min(self, h: int) -> EdgeEvent:
        """
        특정 힙의 최소 값을 반환합니다.
        
        Args:
            h (int): 힙의 인덱스
        
        Returns:
            EdgeEvent: 힙의 최소 값
        """
        return self.node[self.heap[h]].key

    def argmin(self, h: int) -> int:
        """
        특정 힙의 최소 값의 인덱스를 반환합니다.
        
        Args:
            h (int): 힙의 인덱스
        
        Returns:
            int: 최소 값의 인덱스
        """
        return self.heap[h]

    def pop(self, h: int) -> None:
        """
        특정 힙에서 최소 값을 제거합니다.
        
        Args:
            h (int): 힙의 인덱스
        """
        self.erase(h, self.heap[h])

    def push(self, h: int, v: int, key: EdgeEvent) -> None:
        """
        새로운 노드를 힙에 추가합니다.
        
        Args:
            h (int): 힙의 인덱스
            v (int): 추가할 노드의 인덱스
            key (EdgeEvent): 노드의 키 값
        """
        self.node[v] = self.Node(key)
        self.heap[h] = self._merge(self.heap[h], v)

    def erase(self, h: int, v: int):
        """
        특정 힙에서 노드를 제거합니다.
        
        Args:
            h (int): 힙의 인덱스
            v (int): 제거할 노드의 인덱스
        """

        # 노드가 사용 중인지 확인
        if not self.used(v):
            return

        # 노드의 자식을 병합
        merged_child = self._two_pass_pairing(self.node[v].child)
        
        # 노드가 루트 노드인 경우
        if not self.node[v].prev:

            # 힙의 루트를 병합된 자식으로 설정
            self.heap[h] = merged_child
        
        # 노드가 루트 노드가 아닌 경우
        else:

            # 노드를 힙에서 분리
            self._cut(v)

            # 힙의 루트를 병합된 자식과 병합
            self.heap[h] = self._merge(self.heap[h], merged_child)

        # 노드를 초기화하여 사용되지 않음을 표시
        self.node[v].prev = -1

    def decrease_key(self, h: int, v: int, key: EdgeEvent):
        """
        특정 노드의 키 값을 감소시킵니다.
        
        Args:
            h (int): 힙의 인덱스
            v (int): 키 값을 감소시킬 노드의 인덱스
            key (EdgeEvent): 새로운 키 값
        """

        # 노드가 사용 중인지 확인
        if not self.used(v):

            # 사용 중이 아니면 push를 통해 노드를 추가
            return self.push(h, v, key)
        
        # 노드가 루트 노드인 경우 키 값을 직접 설정
        if not self.node[v].prev:
            self.node[v].key = key

        # 노드가 루트 노드가 아닌 경우        
        else:

            # 노드를 힙에서 분리
            self._cut(v)

            # 새로운 키 값을 설정
            self.node[v].key = key
            
            # 노드를 힙에 병합
            self.heap[h] = self._merge(self.heap[h], v)

    def _clear_rec(self, v: int):
        """
        주어진 노드와 그 자식 노드들을 재귀적으로 초기화합니다.
        
        Args:
            v (int): 초기화할 노드의 인덱스
        """

        # 현재 노드가 존재하는 동안
        while v:

            # 자식 노드가 존재하면 재귀적으로 초기화
            if self.node[v].child:
                self._clear_rec(self.node[v].child)

            # 현재 노드의 prev 값을 -1로 설정하여 초기화
            self.node[v].prev = -1

            # 다음 형제 노드로 이동
            v = self.node[v].next

    def _cut(self, v: int):
        """
        노드 v를 그 부모로부터 분리합니다.
        
        Args:
            v (int): 분리할 노드의 인덱스
        """
        # 부모 노드와 형제 노드의 인덱스를 가져옴
        parent, next_node = self.node[v].prev, self.node[v].next

        # 부모 노드의 자식 노드가 v인 경우 부모 노드의 자식을 next_node로 설정
        if self.node[parent].child == v:
            self.node[parent].child = next_node

        # 부모 노드의 다음 형제가 v인 경우 부모 노드의 다음 형제를 next_node로 설정
        else:
            self.node[parent].next = next_node

        # 형제 노드의 prev 값을 부모 노드로 설정
        self.node[next_node].prev = parent

        # 현재 노드 v의 prev와 next 값을 0으로 초기화
        self.node[v].next = self.node[v].prev = 0

    def _merge(self, left: int, right: int) -> int:
        """
        두 노드를 병합하여 하나의 트리로 만듭니다.
        
        Args:
            left (int): 병합할 첫 번째 노드의 인덱스
            right (int): 병합할 두 번째 노드의 인덱스

        Returns:
            int: 병합된 트리의 루트 노드 인덱스
        """
        
        # left 노드가 없으면 right 노드를 반환
        if not left:
            return right

        # right 노드가 없으면 left 노드를 반환
        if not right:
            return left

        # 두 노드의 키를 비교하여 작은 키를 가진 노드가 루트가 되도록 설정
        if self.node[left].key > self.node[right].key:
            left, right = right, left

        # 오른쪽 노드를 왼쪽 노드의 자식으로 설정
        self.node[right].next = self.node[left].child
        self.node[left].child = self.node[self.node[right].next].prev = right

        # 오른쪽 노드의 부모를 왼쪽 노드로 설정
        self.node[right].prev = left

        # 병합된 트리의 루트 노드 인덱스를 반환
        return left

    def _two_pass_pairing(self, root: int) -> int:
        """
        두 번의 순회를 통해 페어링 힙을 병합하여 하나의 트리로 만듭니다.

        Args:
            root (int): 병합할 트리의 루트 노드 인덱스

        Returns:
            int: 병합된 트리의 루트 노드 인덱스
        """

        # 루트가 없으면 0을 반환
        if not root:
            return 0

        # 첫 번째 순회: 트리를 두 개씩 병합하여 linked list로 연결
        first_pass_root = 0
        a = root
        while a:

            # a의 다음 노드를 가져옴
            next_root = self.node[a].next
            next_a = 0

            # a의 이전 노드와 다음 노드를 초기화
            self.node[a].prev = self.node[a].next = 0

            # next_root가 존재한다면
            if next_root:

                # b의 다음 노드를 가져옴
                next_a = self.node[next_root].next

                # b의 이전 노드와 다음 노드를 초기화
                self.node[next_root].prev = self.node[next_root].next = 0

            # a와 b를 병합
            a = self._merge(a, next_root)

            # 병합된 노드를 first_pass_root에 연결
            self.node[a].next = first_pass_root

            # 다음 순회를 위해 변수 업데이트
            a, first_pass_root = next_a, a

        # 두 번째 순회: 병합된 트리들을 다시 병합
        second_pass_root = first_pass_root
        s = self.node[first_pass_root].next

        # first_pass_root의 다음 노드를 초기화
        self.node[first_pass_root].next = 0

        while s:

            # s의 다음 노드를 가져옴
            t = self.node[s].next

            # s의 다음 노드를 초기화
            self.node[s].next = 0

            # first_pass_root와 s를 병합
            second_pass_root = self._merge(second_pass_root, s)

            # 다음 순회를 위해 변수 업데이트
            s = t

        # 병합된 트리의 루트 노드를 반환
        return second_pass_root

class PriorityQueue:
    """
    우선순위 큐를 구현하는 클래스입니다.
    이 클래스는 최소 힙(min heap)을 기반으로 하여 우선순위가 높은(작은) 항목을 빠르게 추출할 수 있습니다.
    """
    def __init__(self):

        # 우선순위 큐 데이터를 저장할 리스트 초기화
        self._data = []

    def min(self) -> EdgeEvent:
        """
        우선순위가 가장 높은(작은) 항목을 반환합니다.
        
        Returns:
            EdgeEvent: 우선순위가 가장 높은 항목
        """

        # _data의 첫 번째 항목이 우선순위가 가장 높은 항목
        return self._data[0]

    def clear(self) -> None:
        """
        우선순위 큐를 초기화하여 비웁니다.
        """

        # _data 리스트를 초기화하여 모든 항목 제거
        self._data.clear()

    def push(self, item: EdgeEvent) -> None:
        """
        새로운 항목을 우선순위 큐에 추가합니다.
        
        Args:
            item (EdgeEvent): 우선순위 큐에 추가할 항목
        """

        # heappush를 사용하여 항목을 최소 힙 구조로 추가
        heappush(self._data, item)

    def pop(self) -> EdgeEvent:
        """
        우선순위가 가장 높은(작은) 항목을 제거하고 반환합니다.
        
        Returns:
            EdgeEvent: 우선순위가 가장 높은 항목
        """

        # _data 리스트가 비어있지 않은 경우 heappop을 사용하여 항목 제거 및 반환
        return heappop(self._data) if self._data else None

    def empty(self) -> bool:
        """
        우선순위 큐가 비어 있는지 확인합니다.
        
        Returns:
            bool: 큐가 비어 있으면 True, 그렇지 않으면 False
        """

        # _data 리스트의 길이가 0인지 확인
        return len(self._data) == 0

class InputEdge:
    """
    입력 그래프의 간선을 나타내는 클래스입니다.
    """

    def __init__(self, frm: int, to: int, cost: int):

        # 간선의 시작 정점
        self.frm = frm

        # 간선의 도착 정점
        self.to = to

        # 간선의 비용
        self.cost = cost
    
    def __lt__(self, rhs: 'InputEdge') -> bool:
        """
        두 간선을 비교하여 순서를 결정합니다.
        
        Args:
            rhs (InputEdge): 비교 대상이 되는 다른 간선
            
        Returns:
            bool: 현재 간선이 비교 대상 간선보다 작은지 여부
        """

        # 시작 정점이 동일한 경우
        if self.frm == rhs.frm:

            # 도착 정점이 동일한 경우 비용을 비교
            if self.to == rhs.to:
                return self.cost < rhs.cost
            
            # 도착 정점을 비교
            return self.to < rhs.to
        
        # 시작 정점을 비교
        return self.frm < rhs.frm


class MaximumWeightedMatching:
    K_SEPARATED, K_INNER, K_FREE, K_OUTER = -2, -1, 0, 1

    class Node:
        class NodeLink:
            def __init__(self, blossom_id: int, vertex_id: int):
                """
                노드 링크를 초기화합니다.

                Args:
                    blossom_id (int): 링크된 블로섬의 ID
                    vertex_id (int): 링크된 정점의 ID
                """

                # 링크된 블로섬의 ID
                self.b = blossom_id

                # 링크된 정점의 ID
                self.v = vertex_id

        def __init__(self, u: int):
            """
            노드를 초기화합니다.

            Args:
                u (int): 노드의 ID
            """

            # 부모 노드의 ID
            self.parent = 0

            # 노드 크기
            self.size = 1

            # 링크 배열
            self.link = [self.NodeLink(u, u), self.NodeLink(u, u)]

        def next_v(self) -> int:
            """
            다음 정점의 ID를 반환합니다.

            Returns:
                int: 다음 정점의 ID
            """

            # 첫 번째 링크의 정점 ID 반환
            return self.link[0].v

        def next_b(self) -> int:
            """
            다음 블로섬의 ID를 반환합니다.

            Returns:
                int: 다음 블로섬의 ID
            """

            # 첫 번째 링크의 블로섬 ID 반환
            return self.link[0].b

        def prev_v(self) -> int:
            """
            이전 정점의 ID를 반환합니다.

            Returns:
                int: 이전 정점의 ID
            """

            # 두 번째 링크의 정점 ID 반환
            return self.link[1].v

        def prev_b(self) -> int:
            """
            이전 블로섬의 ID를 반환합니다.

            Returns:
                int: 이전 블로섬의 ID
            """

            # 두 번째 링크의 블로섬 ID 반환
            return self.link[1].b
    
    class Link:
        def __init__(self, frm: int, to: int):
            """
            두 정점을 연결하는 링크를 초기화합니다.

            Args:
                frm (int): 링크의 시작 정점 ID
                to (int): 링크의 끝 정점 ID
            """

            # 링크의 시작 정점 ID
            self.frm = frm

            # 링크의 끝 정점 ID
            self.to = to
    
    class Edge:
        def __init__(self, to: int, cost: int):
            """
            그래프의 간선을 초기화합니다.

            Args:
                to (int): 간선이 연결된 정점의 ID
                cost (int): 간선의 비용
            """

            # 간선이 연결된 정점의 ID
            self.to = to

            # 간선의 비용
            self.cost = cost

    class Event:
        def __init__(self, time: int, id: int):
            """
            이벤트 객체를 초기화합니다.

            Args:
                time (int): 이벤트 발생 시간
                id (int): 이벤트 ID
            """

            # 이벤트 발생 시간
            self.time = time

            # 이벤트 ID
            self.id = id
            
        def __lt__(self, rhs: 'MaximumWeightedMatching.Event') -> bool:
            """
            두 이벤트 객체를 비교합니다. 시간 기준으로 비교합니다.

            Args:
                rhs (Event): 비교할 다른 이벤트 객체

            Returns:
                bool: 현재 객체의 시간이 더 작으면 True, 그렇지 않으면 False
            """

            return self.time < rhs.time
        
        def __gt__(self, rhs: 'MaximumWeightedMatching.Event') -> bool:
            """
            두 이벤트 객체를 비교합니다. 시간 기준으로 비교합니다.

            Args:
                rhs (Event): 비교할 다른 이벤트 객체

            Returns:
                bool: 현재 객체의 시간이 더 크면 True, 그렇지 않으면 False
            """

            return self.time > rhs.time

    def __init__(self, n: int, edgelist: list[InputEdge]):
        """
        Args:
            n (int): 노드의 개수.
            edgelist (list[InputEdge]): 각 간선이 시작 노드, 끝 노드, 가중치를 포함하는 입력 간선 리스트.
        """
        
        # 노드의 개수
        self.N = n

        # 가능한 블로섬의 수
        self.B = (self.N - 1) // 2

        # 노드와 블로섬, 더미 노드를 포함한 총 슬롯 수
        self.S = self.N + self.B + 1

        # 인접 리스트 구성을 관리하기 위한 오프셋 배열
        self.offset = [0 for _ in range(self.N + 2)]

        # 무향 그래프이므로 입력 간선의 두 배 크기로 배열 초기화
        self.edges: list[MaximumWeightedMatching.Edge] = [None for _ in range(len(edgelist) << 1)]

        # 우선순위 큐 초기화
        self.BinaryHeap_EdgeEvent = BinaryHeap(self.S, isEdgeEvent=True)
        self.PairingHeaps = PairingHeaps(self.S, self.S)
        self.PriorityQueue = PriorityQueue()
        self.BinaryHeap_int = BinaryHeap(self.S, isEdgeEvent=False)

        # 각 노드의 간선 수를 오프셋 배열에 채우기
        for edge in edgelist:
            self.offset[edge.frm + 1] += 1
            self.offset[edge.to + 1] += 1

        # 누적 오프셋을 계산하여 각 노드의 간선 시작 인덱스 얻어오기
        self.offset = list(accumulate(self.offset))

        # 입력 간선 리스트에서 간선 배열 채우기
        for edge in edgelist:
            self.edges[self.offset[edge.frm]] = self.Edge(edge.to, edge.cost << 1)
            self.offset[edge.frm] += 1

            self.edges[self.offset[edge.to]] = self.Edge(edge.frm, edge.cost << 1)
            self.offset[edge.to] += 1

        # offset 배열 복원
        for i in range(self.N + 1, 0, -1):
            self.offset[i] = self.offset[i - 1]
        self.offset[0] = 0
    
    def maximum_weighted_matching(self) -> tuple[int, list[int]]:
        """
        최대 가중치를 가지는 매칭을 찾습니다.
        
        알고리즘을 초기화하고, 각 노드에 대한 잠재력을 설정한 후, 
        각 노드가 매칭되지 않은 경우 Edmonds 검색을 수행합니다.
        
        Returns:
            tuple[int, list[int]]: 매칭의 총 가중치와 매칭된 노드들의 리스트를 반환합니다.
        """

        # 알고리즘 초기화
        self.initialize()
        
        # 각 노드의 잠재력 설정
        self.set_potential()
        
        # 각 노드에 대해 매칭되지 않은 경우 Edmonds 검색 수행
        for u in range(1, self.N + 1):
            if not self.mate[u]:
                self.do_edmonds_search(u)
        
        # 최적의 값을 계산하고 매칭된 노드 리스트와 함께 반환
        return (self.calculate_total_weight(), self.mate)

    def calculate_total_weight(self) -> int:
        """
        최적 매칭의 총 가중치를 계산합니다.
        
        Returns:
            int: 매칭의 총 가중치
        """

        ret = 0
        
        # 각 노드 u에 대해
        for u in range(1, self.N + 1):

            # 매칭된 노드의 인덱스가 u보다 큰 경우
            if self.mate[u] > u:
                max_cost = 0

                # u에 연결된 모든 간선 중 매칭된 간선의 비용을 찾음
                for edge_id in range(self.offset[u], self.offset[u + 1]):
                    if self.edges[edge_id].to == self.mate[u]:
                        max_cost = max(max_cost, self.edges[edge_id].cost)

                # 최대 비용을 더함
                ret += max_cost
                
        # 최종 비용을 2로 나눈 값 반환 (비용이 두 배로 저장되어 있으므로)
        return ret >> 1
    
    def reduced_cost(self, u: int, v: int, w: int) -> int:
        """
        간선 (u, v)의 감소 비용을 계산합니다.
        
        잠재력을 사용하여 간선의 실제 비용을 줄여 계산합니다.
        
        Args:
            u (int): 간선의 시작 노드
            v (int): 간선의 도착 노드
            w (int): 간선의 비용
        
        Returns:
            int: 감소 비용
        """

        # 감소 비용 계산: 간선의 실제 비용에서 두 노드의 잠재력 합을 뺀 값
        return self.potential[u] + self.potential[v] - w

    def rematch(self, v: int, w: int) -> None:
        """
        재매칭을 수행하여 매칭 구조를 갱신합니다.
        
        주어진 노드 v를 w와 매칭하고, 재귀적으로 연결된 다른 노드들의 매칭도 갱신합니다.
        
        Args:
            v (int): 재매칭할 노드
            w (int): 노드 v와 매칭할 노드
        """

        # 현재 노드 v의 매칭 상대를 t로 저장
        t = self.mate[v]
        
        # 노드 v를 노드 w와 매칭
        self.mate[v] = w

        # 노드 t가 노드 v와 매칭되지 않았다면 종료
        if self.mate[t] != v:
            return
        
        # 노드 v의 링크가 자기 자신으로 연결된 경우
        if self.link[v].to == self.surface[self.link[v].to]:

            # 노드 t를 노드 v의 from과 매칭
            self.mate[t] = self.link[v].frm

            # 노드 t와 다시 재매칭
            self.rematch(self.mate[t], t)

        # 아닌 경우 노드 v의 from과 to를 각각 재매칭
        else:
            self.rematch(self.link[v].frm, self.link[v].to)
            self.rematch(self.link[v].to, self.link[v].frm)
    
    def fix_mate_and_base(self, blossom_id: int) -> None:
        """
        주어진 블로섬의 매칭과 기본 노드를 수정합니다.
        
        블로섬이 확장될 때, 블로섬 내의 각 노드와 그 매칭 상태를 올바르게 설정하여
        알고리즘이 정확히 작동하도록 합니다.
        
        Args:
            blossom_id (int): 수정할 블로섬의 ID
        """

        # b가 기본 노드의 인덱스 범위 안에 있다면 아무 작업도 하지 않음
        if blossom_id <= self.N:
            return
        
        # 블로섬의 기본 노드
        base_vertex = self.base[blossom_id]

        # 매칭 상태를 수정할 노드와 블로섬을 초기화
        matched_vertex, matched_blossom = self.node[base_vertex].link[0].v, self.node[base_vertex].link[0].b
        direction = self.node[matched_blossom].link[1].v != self.mate[matched_vertex]

        while True:

            # 블로섬 내의 다음 노드와 블로섬을 찾음
            matched_vertex, matched_blossom = self.node[base_vertex].link[direction].v, self.node[base_vertex].link[direction].b

            # 매칭 상태가 다른 경우 루프를 종료
            if self.node[matched_blossom].link[1 ^ direction].v != self.mate[matched_vertex]:
                break

            # 블로섬 bv와 bmv의 매칭과 기본 노드를 수정
            self.fix_mate_and_base(base_vertex)
            self.fix_mate_and_base(matched_blossom)

            # base_vertex를 다음 블로섬으로 갱신
            base_vertex = self.node[matched_blossom].link[direction].b

        # 블로섬의 기본 노드를 갱신
        self.base[blossom_id] = base_vertex

        # 블로섬의 매칭을 갱신
        self.fix_mate_and_base(base_vertex)

        # 블로섬의 매칭을 설정
        self.mate[blossom_id] = self.mate[base_vertex]

    def reset_time(self) -> None:
        """
        현재 시간을 초기화하고, 첫 번째 이벤트를 무한대로 설정합니다.
        
        알고리즘이 실행되는 동안 이벤트 타이머를 초기화하여
        다음 이벤트를 기다리는 상태로 설정합니다.
        """

        # 현재 시간 초기화
        self.current_time = 0

        # 이벤트값 초기화
        self.event = self.Event(inf, 0)

    def reset_blossom(self, blossom_id: int) -> None:
        """
        주어진 블로섬의 상태를 초기화합니다.
        
        각 블로섬의 레이블을 자유(K_FREE) 상태로 설정하고,
        링크를 초기화하며, 슬랙 값을 무한대로 설정하고,
        지연 값을 0으로 초기화합니다.
        
        Args:
            blossom_id (int): 초기화할 블로섬의 ID.
        """

        # 블로섬 레이블을 K_FREE 상태로 설정
        self.label[blossom_id] = self.K_FREE

        # 블로섬의 링크를 초기화
        self.link[blossom_id].frm = 0
        self.link[blossom_id].to = 0

        # 슬랙 값을 무한대로 설정
        self.slack[blossom_id] = inf

        # 지연 값을 0으로 초기화
        self.lazy[blossom_id] = 0
    
    def reset_all(self) -> None:
        """
        모든 노드와 블로섬의 상태를 초기화합니다.

        각 노드와 블로섬의 레이블을 초기 상태로 설정하고,
        잠재력과 슬랙 값을 초기화하며, 힙을 비웁니다.
        """

        # 0번 노드를 자유 상태로 설정
        self.label[0] = self.K_FREE
        self.link[0].frm = 0

        # 1번 노드부터 N번 노드까지 순회
        for v in range(1, self.N + 1):
            if self.label[v] == self.K_OUTER:

                # OUTER 노드는 현재 시간을 잠재력에서 뺌
                self.potential[v] -= self.current_time
            else:

                # 나머지 노드는 지연 값을 잠재력에 더함
                self.potential[v] += self.lazy[self.surface[v]]

                # 노드가 INNER 상태인 경우 현재 시간과 생성 시간의 차이를 더함
                if self.label[self.surface[v]] == self.K_INNER:
                    self.potential[v] += self.current_time - self.time_created[self.surface[v]]

            # 각 노드의 블로섬 상태를 초기화
            self.reset_blossom(v)

        # 블로섬 인덱스 및 남은 블로섬 개수 설정
        b, r = self.N + 1, self.B - self.unused_blossom_id_index
        while r > 0 and b < self.S:
            if self.base[b] != b:
                if self.surface[b] == b:

                    # 매칭과 블로섬의 베이스를 설정
                    self.fix_mate_and_base(b)

                    # 블로섬의 상태에 따라 잠재력 갱신
                    if self.label[b] == self.K_OUTER:
                        self.potential[b] += (self.current_time - self.time_created[b]) << 1
                    elif self.label[b] == self.K_INNER:
                        self.fix_blossom_potential(self.K_INNER, b)
                    else:
                        self.fix_blossom_potential(self.K_FREE, b)

                # 블로섬의 힙을 초기화
                self.PairingHeaps.clear(b)
                self.reset_blossom(b)
                r -= 1
            b += 1

        # 큐와 힙을 초기화
        self.queue.clear()
        self.reset_time()
        self.BinaryHeap_EdgeEvent.clear()
        self.PriorityQueue.clear()
        self.BinaryHeap_int.clear()
    
    def do_edmonds_search(self, root: int) -> None:
        """
        Edmonds의 매칭 알고리즘을 사용하여 최대 가중치 매칭을 찾습니다.

        주어진 루트 노드에서 시작하여 매칭을 확장하고,
        이중 변수와 슬랙 값을 조정하여 최적의 매칭을 찾습니다.
        
        Args:
            root (int): 매칭을 시작할 루트 노드
        """

        # 루트 노드의 잠재력이 0인 경우 탐색을 중지
        if self.potential[root] == 0:
            return

        # 루트 노드를 시작으로 블로섬 링크를 설정하고 외부 노드로 표시
        self.link_blossom(self.surface[root], self.Link(0, 0))

        # 루트 노드를 외부 노드로 설정하고 잠재력 조정
        self.push_outer_and_fix_potentials(self.surface[root], 0)

        while True:

            # 매칭이 성공적으로 이루어진 경우 루프 탈출
            if self.augment(root):
                break

            # 이중 변수를 조정하고 매칭이 이루어진 경우 루프 탈출
            if self.adjust_dual_variables(root):
                break

        # 모든 상태 초기화
        self.reset_all()
    
    def fix_blossom_potential(self, lab: int, blossom_id: int) -> int:
        """
        블로섬의 잠재력을 수정하여 이중 변수와 잠재력 값을 갱신합니다.
        
        블로섬의 레이블에 따라 잠재력을 조정하여 
        알고리즘의 효율성과 정확성을 높입니다.
        
        Args:
            lab (int): 블로섬의 레이블 (K_INNER, K_OUTER, K_FREE 중 하나)
            blossom_id (int): 블로섬의 ID
        
        Returns:
            int: 조정된 잠재력 값
        """

        # 블로섬의 지연 값을 가져옴
        delta = self.lazy[blossom_id]

        # 블로섬의 지연 값을 초기화
        self.lazy[blossom_id] = 0

        # 블로섬의 레이블이 INNER인 경우
        if lab == self.K_INNER:

            # 현재 시간에서 블로섬이 생성된 시간을 뺀 값을 계산
            dt = self.current_time - self.time_created[blossom_id]

            # 블로섬이 노드 개수를 초과하는 경우
            if blossom_id > self.N:

                # 블로섬의 잠재력을 조정
                self.potential[blossom_id] -= dt << 1

            # 잠재력에 조정 값을 추가
            delta += dt

        return delta

    def update_heap_event_edge(self, lab: int, x: int, y: int, by: int, t: int) -> None:
        """
        주어진 블로섬의 heap_edge_event 값을 업데이트합니다.
        
        새로운 경로의 슬랙 값을 갱신하고, 필요하면 heap_edge_event 또는 heap_blossom_edge_event에 값을 추가합니다.
        
        Args:
            lab (int): 블로섬의 레이블 (K_INNER, K_OUTER, K_FREE 중 하나)
            x (int): 출발 노드
            y (int): 도착 노드
            by (int): 도착 블로섬
            t (int): 슬랙 값
        """
        
        # 슬랙 값이 기존 슬랙 값보다 작지 않으면 업데이트할 필요 없음
        if t >= self.slack[y]:
            return

        # 슬랙 값과 최적 경로 출발 노드를 갱신
        self.slack[y] = t
        self.best_from[y] = x

        # 도착 노드와 도착 블로섬이 같은 경우
        if y == by:

            # 레이블이 INNER가 아닌 경우 heap_edge_event에 값을 추가
            if lab != self.K_INNER:
                self.BinaryHeap_EdgeEvent.decrease_key(y, EdgeEvent(t + self.lazy[y], x, y))
        else:

            # 도착 블로섬의 그룹 값을 가져옴
            gy = self.group[y]

            # 그룹 값이 도착 노드와 다르면 슬랙 값을 갱신하고 heap_blossom_edge_event에 값을 추가
            if gy != y:
                if t >= self.slack[gy]:
                    return
                self.slack[gy] = t
            self.PairingHeaps.decrease_key(by, gy, EdgeEvent(t, x, y))

            # 레이블이 INNER인 경우 함수 종료
            if lab == self.K_INNER:
                return
            
            # heap_blossom_edge_event에서 최솟값을 가져와 heap_edge_event에 값을 추가
            m = self.PairingHeaps.min(by)
            self.BinaryHeap_EdgeEvent.decrease_key(by, EdgeEvent(m.time + self.lazy[by], m.frm, m.to))
    
    def activate_heap_edge_event_node(self, blossom_id: int) -> None:
        """
        주어진 블로섬 노드를 활성화하여 heap_edge_event에 추가합니다.
        
        Args:
            b (int): 블로섬 노드의 인덱스
        """
        
        # 노드가 N보다 작거나 같은 경우
        if blossom_id <= self.N:

            # 슬랙 값이 무한대가 아니면 heap_edge_event에 추가
            if self.slack[blossom_id] < inf:
                self.BinaryHeap_EdgeEvent.push(blossom_id, EdgeEvent(self.slack[blossom_id] + self.lazy[blossom_id], self.best_from[blossom_id], blossom_id))
        else:

            # heap_blossom_edge_event가 비어있지 않으면 최솟값을 heap_edge_event에 추가
            if not self.PairingHeaps.empty(blossom_id):
                m = self.PairingHeaps.min(blossom_id)
                self.BinaryHeap_EdgeEvent.push(blossom_id, EdgeEvent(m.time + self.lazy[blossom_id], m.frm, m.to))
    
    def swap_blossom(self, b1: int, b2: int) -> None:
        """
        두 블로섬의 정보를 교환합니다.
        
        Args:
            b1 (int): 첫 번째 블로섬의 인덱스
            b2 (int): 두 번째 블로섬의 인덱스
        """
        
        # 기본(base) 노드를 교환
        self.base[b1], self.base[b2] = self.base[b2], self.base[b1]
        if self.base[b1] == b1:
            self.base[b1] = b2
        
        # 무거운 노드(heavy node)를 교환
        self.heavy[b1], self.heavy[b2] = self.heavy[b2], self.heavy[b1]
        if self.heavy[b1] == b1:
            self.heavy[b1] = b2
        
        # 연결 정보를 교환
        self.link[b1], self.link[b2] = self.link[b2], self.link[b1]
        
        # 짝을 이루는 노드를 교환
        self.mate[b1], self.mate[b2] = self.mate[b2], self.mate[b1]
        
        # 잠재력 값을 교환
        self.potential[b1], self.potential[b2] = self.potential[b2], self.potential[b1]
        
        # 지연 값을 교환
        self.lazy[b1], self.lazy[b2] = self.lazy[b2], self.lazy[b1]
        
        # 생성 시간을 교환
        self.time_created[b1], self.time_created[b2] = self.time_created[b2], self.time_created[b1]
        
        # 두 노드의 연결 정보를 업데이트
        for d in range(2):
            self.node[self.node[b1].link[d].b].link[d ^ 1].b = b2
        
        # 두 노드 객체 자체를 교환
        self.node[b1], self.node[b2] = self.node[b2], self.node[b1]
    
    def set_surface_and_group(self, blossom_id: int, surface: int, group: int) -> None:
        """
        블로섬 내부의 모든 노드와 블로섬 자체에 대해 surface와 group 값을 설정합니다.
        
        Args:
            blossom_id (int): 블로섬의 인덱스
            surface (int): 설정할 surface 값
            group (int): 설정할 group 값
        """

        # 현재 블로섬 b의 surface와 group을 설정
        self.surface[blossom_id] = surface
        self.group[blossom_id] = group
        
        # b가 실제 노드인 경우, 블로섬 내부의 노드들을 순회하면서 surface와 group 값을 설정
        if blossom_id > self.N:
            based_b = self.base[blossom_id]
            while self.surface[based_b] != surface:
                
                # 재귀적으로 내부 노드들의 surface와 group 값을 설정
                self.set_surface_and_group(based_b, surface, group)

                # 다음 노드로 이동
                based_b = self.node[based_b].next_b()
    
    def merge_smaller_blossoms(self, blossom_id: int) -> None:
        """
        블로섬 내의 작은 블로섬들을 병합하여 큰 블로섬을 만듭니다.
        
        Args:
            blossom_id (int): 병합할 블로섬의 인덱스
        """
        # 가장 큰 블로섬의 인덱스
        largest_blossom_id = blossom_id

        # 가장 큰 블로섬의 크기
        largest_size = 1

        # 블로섬 내의 모든 노드를 순회하면서 가장 큰 블로섬 찾기
        beta = b = self.base[blossom_id]
        while True:

            # 현재 노드의 크기가 가장 큰 블로섬보다 크면 업데이트
            if self.node[b].size > largest_size:
                largest_size = self.node[b].size
                largest_blossom_id = b
                
            # 순회 종료 조건
            if (b := self.node[b].next_b()) == beta:
                break

        # 작은 블로섬들을 순회하면서 가장 큰 블로섬으로 병합
        beta = b = self.base[blossom_id]
        while True:
            if b != largest_blossom_id:
                self.set_surface_and_group(b, largest_blossom_id, b)
            if (b := self.node[b].next_b()) == beta:
                break

        # 그룹 설정
        self.group[largest_blossom_id] = largest_blossom_id

        # 가장 큰 블로섬의 크기가 1보다 크면 병합
        if largest_size > 1:
            self.surface[blossom_id] = largest_blossom_id
            self.heavy[blossom_id] = largest_blossom_id
            self.swap_blossom(largest_blossom_id, blossom_id)
        else:
            self.heavy[blossom_id] = 0
    
    def contract(self, x: int, y: int, edge_id: int) -> None:
        """
        두 노드를 포함하는 블로섬을 축소(Contract)하여 새로운 블로섬을 생성합니다.
        
        Args:
            x (int): 첫 번째 노드의 인덱스
            y (int): 두 번째 노드의 인덱스
            edge_id (int): 두 노드를 연결하는 간선의 인덱스
        """

        # x와 y의 블로섬 루트를 찾음
        bx, by = self.surface[x], self.surface[y]

        # 간선 id로 새로운 값 설정
        h = -(edge_id + 1)

        # mate로 연결된 노드 업데이트
        self.link[self.surface[self.mate[bx]]].frm = h
        self.link[self.surface[self.mate[by]]].frm = h

        # 최소 공통 조상(LCA)을 찾는 루프
        while True:
            if self.mate[by]:
                bx, by = by, bx
            bx = lca = self.surface[self.link[bx].frm]
            if self.link[self.surface[self.mate[bx]]].frm == h:
                break
            self.link[self.surface[self.mate[bx]]].frm = h
        
        # 새로운 블로섬의 인덱스를 가져옴
        self.unused_blossom_id_index -= 1
        blossom_id = self.unused_blossom_id[self.unused_blossom_id_index]

        # 블로섬 트리의 크기를 초기화
        tree_size = 0

        # 두 블로섬을 하나의 블로섬으로 합치는 과정
        for d in range(2):
            blossom_vertex = self.surface[x]
            while blossom_vertex != lca:
                mate_vertex = self.mate[blossom_vertex]
                blossom_mate_vertex, v = self.surface[mate_vertex], self.mate[mate_vertex]
                frm, to = self.link[v].frm, self.link[v].to

                # 블로섬의 크기 업데이트
                tree_size += self.node[blossom_vertex].size + self.node[blossom_mate_vertex].size

                # 새로운 링크 설정
                self.link[mate_vertex] = self.Link(x, y)
                
                # 잠재력 업데이트
                if blossom_vertex > self.N:
                    self.potential[blossom_vertex] += (self.current_time - self.time_created[blossom_vertex]) << 1
                if blossom_mate_vertex > self.N:
                    self.BinaryHeap_int.erase(blossom_mate_vertex)

                # 외부 블로섬과 잠재력을 업데이트
                self.push_outer_and_fix_potentials(blossom_mate_vertex, self.fix_blossom_potential(self.K_INNER, blossom_mate_vertex))

                # 블로섬 간 링크 설정 (bv를 bmv로 연결)
                self.node[blossom_vertex].link[d] = self.Node.NodeLink(blossom_mate_vertex, mate_vertex)
                self.node[blossom_mate_vertex].link[d ^ 1] = self.Node.NodeLink(blossom_vertex, v)

                # 다음 블로섬의 표면 업데이트
                blossom_vertex = self.surface[frm]

                # 다음 링크 설정
                self.node[blossom_mate_vertex].link[d] = self.Node.NodeLink(blossom_vertex, frm)
                self.node[blossom_vertex].link[d ^ 1] = self.Node.NodeLink(blossom_mate_vertex, to)

            # 외부 블로섬 링크 설정
            self.node[self.surface[x]].link[d ^ 1] = self.Node.NodeLink(self.surface[y], y)

            # x와 y를 교체하여 다음 반복에서 처리
            x, y = y, x

        # LCA가 노드 수보다 크다면 잠재력 업데이트
        if lca > self.N:
            self.potential[lca] += (self.current_time - self.time_created[lca]) << 1
        
        # 새로운 블로섬의 크기, base, link, matching 설정
        self.node[blossom_id].size = tree_size + self.node[lca].size
        self.base[blossom_id] = lca
        self.link[blossom_id] = self.link[lca]
        self.mate[blossom_id] = self.mate[lca]
        self.label[blossom_id] = self.K_OUTER
        self.surface[blossom_id] = blossom_id
        self.time_created[blossom_id] = self.current_time
        self.potential[blossom_id] = 0
        self.lazy[blossom_id] = 0

        # 작은 블로섬들을 병합
        self.merge_smaller_blossoms(blossom_id)

    def link_blossom(self, v: int, link: Link) -> None:
        """
        주어진 노드를 블로섬에 연결합니다.
        
        Args:
            v (int): 노드의 인덱스
            link (Link): 연결할 링크 정보 (frm, to)
        """

        # 노드 v에 대한 링크를 설정
        self.link[v] = self.Link(link.frm, link.to)
        
        # v가 단일 노드라면 종료
        if v <= self.N:
            return
        
        # 블로섬의 베이스 노드(b)를 가져옴
        base_vertex = self.base[v]

        # 블로섬의 베이스 노드(b)와 링크 정보를 설정
        self.link_blossom(base_vertex, link)
        
        # 이전 블로섬 노드(pb)를 가져옴
        prev_base_vertex = self.node[base_vertex].prev_b()

        # 현재 블로섬의 이전 노드(v)를 기준으로 링크 정보 설정
        link = self.Link(self.node[prev_base_vertex].next_v(), self.node[base_vertex].prev_v())

        # 블로섬의 베이스 노드(bv)를 가져옴
        bv = base_vertex

        # 순환 구조를 유지하면서 링크 설정
        while True:

            # 다음 블로섬 노드(bw)를 가져옴
            bw = self.node[bv].next_b()

            # bw가 현재 블로섬의 베이스 노드(b)와 같다면 종료
            if bw == base_vertex:
                break

            # 블로섬 bw에 링크 설정
            self.link_blossom(bw, link)

            # 다음 블로섬 노드(nb)를 기준으로 링크 정보 설정
            nl = self.Link(self.node[bw].prev_v(), self.node[bv].next_v())
            
            # bv를 다음 블로섬 노드로 업데이트
            bv = self.node[bw].next_b()
            
            # 블로섬 bv에 링크 설정
            self.link_blossom(bv, nl)

    def push_outer_and_fix_potentials(self, v: int, d: int) -> None:
        """
        주어진 노드를 외부 노드로 설정하고 잠재력을 갱신합니다.
        
        Args:
            v (int): 노드의 인덱스
            d (int): 추가할 잠재력 값
        """

        # 노드 v를 외부 노드로 설정
        self.label[v] = self.K_OUTER

        # 노드 v가 블로섬이면 내부 노드를 반복하여 모두 외부 노드로 설정
        if v > self.N:
            base_vertex = self.base[v]
            while self.label[base_vertex] != self.K_OUTER:
                self.push_outer_and_fix_potentials(base_vertex, d)
                base_vertex = self.node[base_vertex].next_b()

        # 노드 v가 블로섬이 아니면 잠재력 값을 갱신
        else:
            self.potential[v] += self.current_time + d
            if self.potential[v] < self.event.time:

                # event를 갱신
                self.event = self.Event(self.potential[v], v)

            # 큐에 노드 v를 추가
            self.queue.append(v)
    
    def grow(self, root: int, x: int, y: int) -> bool:
        """
        매칭을 확장하여 새로운 매칭 경로를 생성하는 함수입니다.

        Args:
            root (int): 탐색의 시작 노드 (루트 노드)
            x (int): 현재 확장 중인 노드
            y (int): 연결할 노드

        Returns:
            bool: 매칭이 성공적으로 이루어진 경우 True, 그렇지 않으면 False
        """

        # y 노드의 대표 블로섬을 가져옴
        by = self.surface[y]

        # y 노드가 이미 방문되었는지 확인
        visited = self.label[by] != self.K_FREE

        # y 노드가 방문되지 않았으면 링크 초기화
        if not visited:
            self.link_blossom(by, self.Link(0, 0))

        # y 노드를 내부 노드로 설정
        self.label[by] = self.K_INNER

        # 현재 시간을 저장
        self.time_created[by] = self.current_time

        # y 노드를 힙에서 제거
        self.BinaryHeap_EdgeEvent.erase(by)

        # y 노드와 y 노드의 대표 블로섬이 다를 경우 잠재력 힙 갱신
        if y != by:
            self.BinaryHeap_int.update(by, self.current_time + (self.potential[by] >> 1))

        # y 노드와 매칭된 노드 가져오기
        z = self.mate[by]

        # y 노드가 매칭되지 않은 경우 매칭 시도
        if z == 0 and by != self.surface[root]:

            # 매칭 성공 시 매칭 경로 업데이트
            self.rematch(x, y)
            self.rematch(y, x)

            # 매칭 성공
            return True
        
        # z 노드의 대표 블로섬 가져오기
        bz = self.surface[z]

        # z 노드가 방문되지 않았으면 링크 초기화
        if not visited:
            self.link_blossom(bz, self.Link(x, y))

        # z 노드가 이미 방문되었으면
        else:

            # 링크 업데이트
            self.link[bz] = self.Link(x, y)

            # z 노드와 매칭된 노드도 링크 업데이트
            self.link[z] = self.Link(x, y)

        # z 노드를 외부 노드로 설정 및 잠재력 갱신
        self.push_outer_and_fix_potentials(bz, self.fix_blossom_potential(self.K_FREE, bz))

        # 현재 시간 저장
        self.time_created[bz] = self.current_time

        # z 노드를 힙에서 제거
        self.BinaryHeap_EdgeEvent.erase(bz)

        # 매칭 실패
        return False

    def free_blossom(self, blossom_id: int) -> None:
        """
        주어진 블로섬 ID를 사용되지 않은 블로섬 리스트에 추가하여 해제합니다.

        Args:
            bid (int): 해제할 블로섬 ID
        """

        # 사용되지 않은 블로섬 리스트에 추가
        self.unused_blossom_id[self.unused_blossom_id_index] = blossom_id

        # 사용되지 않은 블로섬 인덱스 증가
        self.unused_blossom_id_index += 1

        # 블로섬의 기본 노드를 자기 자신으로 설정
        self.base[blossom_id] = blossom_id

    def recalculate_minimum_slack(self, blossom_id: int, group_id: int) -> int:
        """
        블로섬 b의 최소 슬랙 값을 재계산합니다.
        
        Args:
            blossom_id (int): 슬랙 값을 재계산할 블로섬 ID
            group_id (int): 그룹 ID
        
        Returns:
            int: 최소 슬랙 값을 갖는 노드 ID
        """

        # 기본 노드일 경우 슬랙 값이 현재 그룹의 슬랙 값보다 작으면 갱신
        if blossom_id <= self.N:
            
            # 슬랙 값이 더 크거나 같으면 0 반환
            if self.slack[blossom_id] >= self.slack[group_id]:
                return 0
            
            # 그룹 슬랙 값을 현재 노드의 슬랙 값으로 갱신
            self.slack[group_id] = self.slack[blossom_id]

            # 최소 슬랙 값을 갖는 노드로 갱신
            self.best_from[group_id] = self.best_from[blossom_id]

            # 최소 슬랙 값을 갖는 노드 ID 반환
            return blossom_id
        
        # 최소 슬랙 값을 갖는 노드 ID 초기화
        v = 0

        # 블로섬의 기본 노드를 가져옴
        start_blossom = base_blossom = self.base[blossom_id]
        
        while True:

            # 슬랙 값이 갱신되면 최소 슬랙 값을 갖는 노드 ID 갱신
            if (w := self.recalculate_minimum_slack(base_blossom, group_id)) != 0:
                v = w

            # 다음 블로섬이 초기 블로섬과 같아지면 반복 종료
            if (base_blossom := self.node[base_blossom].next_b()) == start_blossom:
                break

        # 최소 슬랙 값을 갖는 노드 ID 반환
        return v

    def construct_smaller_components(self, blossom_id: int, surface_id: int, group_id: int) -> None:
        """
        주어진 블로섬을 구성하는 작은 컴포넌트들을 설정합니다.
        
        Args:
            blossom_id (int): 블로섬 ID
            surface_id (int): 표면(surface) 노드 ID
            group_id (int): 그룹 ID
        """

        # 블로섬의 표면 노드와 그룹을 설정
        self.surface[blossom_id], self.group[blossom_id] = surface_id, group_id

        # b가 기본 노드인 경우 종료
        if blossom_id <= self.N:
            return
        
        # 블로섬의 기본 노드를 가져옴
        base_blossom = self.base[blossom_id]

        # base_blossom의 표면 노드가 현재 표면 노드 ID와 달라질때까지 반복
        while self.surface[base_blossom] != surface_id:

            # base_blossom이 블로섬의 무거운 정점인 경우 해당 블로섬을 재귀적으로 처리하여 하위 컴포넌트 설정
            if base_blossom == self.heavy[blossom_id]:
                self.construct_smaller_components(base_blossom, surface_id, group_id)
            
            # 무거운 정점이 아닌 경우 각 블로섬을 독립적으로 설정하여 surface와 group 지정
            else:

                # 기본 노드를 surface_id와 group_id로 설정
                self.set_surface_and_group(base_blossom, surface_id, base_blossom)
                to = 0

                # base_blossom이 기본 노드가 아닌 경우 슬랙 값을 재계산하여 to에 저장
                if base_blossom > self.N:
                    self.slack[base_blossom] = inf
                    to = self.recalculate_minimum_slack(base_blossom, base_blossom)

                # slack 값이 INF 값보다 작은 경우 to에 base_blossom 저장
                elif self.slack[base_blossom] < inf:
                    to = base_blossom

                # to가 0보다 큰 경우, heap_blossom_edge_event에 push
                if to > 0:
                    self.PairingHeaps.push(surface_id, base_blossom, EdgeEvent(self.slack[base_blossom], self.best_from[base_blossom], to))

            # 다음 블로섬으로 이동
            base_blossom = self.node[base_blossom].next_b()
    
    def move_to_largest_blossom(self, blossom_id: int) -> None:
        """
        블로섬을 가장 큰 하위 블로섬으로 이동시키고 그에 따라 구조를 업데이트합니다.

        Args:
            blossom_id (int): 블로섬 ID
        """

        # 블로섬의 무거운 정점을 가져옴
        heavy_blossom = self.heavy[blossom_id]
        
        # 현재 시간과 블로섬의 생성 시간의 차이를 계산하여 지연 값(d)을 구함
        delta = (self.current_time - self.time_created[blossom_id]) + self.lazy[blossom_id]

        # 지연 값을 0으로 초기화
        self.lazy[blossom_id] = 0

        # 블로섬의 기본 노드를 가져옴
        base_blossom = self.base[blossom_id]
        beta = base_blossom

        # 블로섬 내 모든 노드에 대해 반복
        while True:

            # 현재 시간으로 생성 시간을 갱신
            self.time_created[base_blossom] = self.current_time

            # 계산된 지연 값을 설정
            self.lazy[base_blossom] = delta

            # base_blossom이 무거운 정점이 아닌 경우 작은 컴포넌트들을 구성한 뒤 heap_blossom_edge_evnet에서 해당 블로섬을 제거
            if base_blossom != heavy_blossom:
                self.construct_smaller_components(base_blossom, base_blossom, base_blossom)
                self.PairingHeaps.erase(blossom_id, base_blossom)

            # base_blossom이 다시 처음으로 돌아오면 루프 종료
            if (base_blossom := self.node[base_blossom].next_b()) == beta:
                break

        # 무거운 정점이 존재하는 경우
        if heavy_blossom > 0:

            # 무거운 정점과 현재 블로섬을 교환
            self.swap_blossom(heavy_blossom, blossom_id)
            blossom_id = heavy_blossom

        # 현재 블로섬을 사용하지 않는 블로섬으로 설정
        self.free_blossom(blossom_id)
    
    def expand(self, blossom_id: int) -> None:
        """
        블로섬을 확장하여 내부 구조를 해체하고 원래 노드들을 복원합니다.

        Args:
            blossom_id (int): 확장할 블로섬 ID
        """

        # 블로섬의 기본 노드와 짝 노드를 가져옴
        matched_vertex = self.mate[self.base[blossom_id]]

        # 블로섬을 가장 큰 하위 블로섬으로 이동시킴
        self.move_to_largest_blossom(blossom_id)

        # 이전 연결 정보를 저장
        old_link = self.link[matched_vertex]
        old_base = self.surface[self.mate[matched_vertex]]
        root = self.surface[old_link.to]
        direction = self.mate[root] == self.node[root].link[0].v

        # 블로섬의 기본 노드에서 루트까지 경로를 따라가며 노드를 업데이트
        current_base = self.node[old_base].link[direction ^ 1].b
        while current_base != root:

            # 노드의 레이블을 K_SEPARATED로 설정
            self.label[current_base] = self.K_SEPARATED

            # 힙 노드를 활성화
            self.activate_heap_edge_event_node(current_base)

            # 노드 이동
            current_base = self.node[current_base].link[direction ^ 1].b

            # 다음 노드도 K_SEPARATED로 설정
            self.label[current_base] = self.K_SEPARATED

            # 힙 노드를 활성화
            self.activate_heap_edge_event_node(current_base)

            # 노드 이동
            current_base = self.node[current_base].link[direction ^ 1].b

        # 이전 베이스 노드부터 루트까지 경로를 따라가며 노드를 업데이트
        current_base = old_base
        while True:

            # 노드의 레이블을 K_INNER로 설정
            self.label[current_base] = self.K_INNER

            # 현재 노드의 다음 노드를 가져옴
            next_base = self.node[current_base].link[direction].b

            # 현재 노드가 루트인 경우 이전 연결 정보 복원
            if current_base == root:
                self.link[self.mate[current_base]] = old_link

            # 그렇지 않은 경우 다음 노드와의 연결 정보 업데이트
            else:
                self.link[self.mate[current_base]] = self.Link(self.node[current_base].link[direction].v, self.node[next_base].link[direction ^ 1].v)

            # mate 연결 정보 업데이트
            self.link[self.surface[self.mate[current_base]]] = self.link[self.mate[current_base]]

            # 현재 노드가 원래 노드보다 큰 경우 (블로섬인 경우)
            if current_base > self.N:
                if self.potential[current_base] == 0:

                    # 재귀적으로 확장
                    self.expand(current_base)
                else:

                    # 힙에 현재 노드 추가
                    self.BinaryHeap_int.push(current_base, self.current_time + (self.potential[current_base] >> 1))

            # 현재 노드가 루트인 경우 반복문 종료
            if current_base == root:
                break

            # 다음 노드로 이동
            current_base = next_base

            # 다음 노드를 outer로 설정하고 잠재력을 업데이트
            self.push_outer_and_fix_potentials(next_base, self.fix_blossom_potential(self.K_INNER, next_base))

            # 방향을 변경하여 다음 노드로 이동
            current_base = self.node[next_base].link[direction].b

    def augment(self, root: int) -> bool:
        """
        매칭을 확장하여 증가 경로를 찾고 매칭을 개선합니다.

        Args:
            root (int): 현재 검색의 루트 노드

        Returns:
            bool: 증가 경로를 찾았는지 여부를 반환
        """

        # 큐가 비어 있을 때까지 반복
        while self.queue:

            # 큐에서 노드를 가져옴
            x = self.queue.popleft()

            # 현재 노드의 표면 노드
            bx = self.surface[x]

            # 현재 노드의 잠재력이 현재 시간과 동일한 경우
            if self.potential[x] == self.current_time:
                if x != root:

                    # 매칭을 갱신
                    self.rematch(x, 0)

                # 증가 경로를 찾았음을 의미
                return True

            # 현재 노드의 모든 엣지를 탐색
            for edge_id in range(self.offset[x], self.offset[x + 1]):
                edge = self.edges[edge_id]
                y = edge.to
                by = self.surface[y]

                # 두 표면 노드가 동일한 경우 건너뜀
                if bx == by:
                    continue

                # 표면 노드의 레이블을 가져옴
                label = self.label[by]

                # 표면 노드가 outer 노드인 경우
                if label == self.K_OUTER:

                    # 감소 비용을 계산하여 시간 업데이트
                    time = self.reduced_cost(x, y, edge.cost) >> 1

                    # 업데이트된 시간이 현재 시간과 같다면 블로섬을 축소
                    if time == self.current_time:
                        self.contract(x, y, edge_id)
                        bx = self.surface[x]
                    
                    # 업데이트된 시간이 event의 시간보다 작다면 우선순위 큐에 이벤트 추가
                    elif time < self.event.time:
                        self.PriorityQueue.push(EdgeEvent(time, x, edge_id))

                # 표면 노드가 inner 또는 free 노드인 경우
                else:

                    # 감소 비용을 계산하여 시간 업데이트
                    time = self.reduced_cost(x, y, edge.cost)

                    # 시간이 INF라면 스킵
                    if time >= inf:
                        continue

                    # inner가 아닌 경우
                    if label != self.K_INNER:

                        # 시간과 지연 시간 비교
                        if time + self.lazy[by] == self.current_time:

                            # 증가 경로 찾기 시도
                            if self.grow(root, x, y):
                                return True
                        
                        # Free EdgeEvent 업데이트
                        else:
                            self.update_heap_event_edge(self.K_FREE, x, y, by, time)

                    # inner인 경우 매칭이 아닌 경우에 Inner EdgeEvent 업데이트
                    else:
                        if self.mate[x] != y:
                            self.update_heap_event_edge(self.K_INNER, x, y, by, time)

        # 증가 경로를 찾지 못했음을 의미
        return False

    def adjust_dual_variables(self, root: int) -> bool:
        """
        이중 변수(dual variable)를 조정하여 매칭 알고리즘의 다음 단계를 준비합니다.

        Args:
            root (int): 현재 검색의 루트 노드

        Returns:
            bool: 증가 경로를 찾았는지 여부를 반환
        """
        # 네 가지 이벤트의 최소 시간을 찾기 위해 초기화

        # event의 시간
        time1 = self.event.time

        # heap_edge_event의 최소 시간
        time2 = inf if self.BinaryHeap_EdgeEvent.empty() else self.BinaryHeap_EdgeEvent.min().time

        # heap_tight_edge의 최소 시간
        time3 = inf
        while not self.PriorityQueue.empty():
            e = self.PriorityQueue.min()
            x, y = e.frm, self.edges[e.to].to
            if self.surface[x] != self.surface[y]:
                time3 = e.time
                break
            else:
                self.PriorityQueue.pop()

        # heap_node_potential의 최소 시간
        time4 = inf if self.BinaryHeap_int.empty() else self.BinaryHeap_int.min()

        # 현재 시간 업데이트
        self.current_time = min(time1, time2, time3, time4)

        # time1 이벤트가 발생한 경우
        if self.current_time == self.event.time:
            x = self.event.id
            if x != root:
                self.rematch(x, 0) # 매칭 갱신
            return True

        # edge_event_heap에서 최소 시간 이벤트를 처리
        while not self.BinaryHeap_EdgeEvent.empty() and self.BinaryHeap_EdgeEvent.min().time == self.current_time:
            x, y = self.BinaryHeap_EdgeEvent.min().frm, self.BinaryHeap_EdgeEvent.min().to
            if self.grow(root, x, y):
                return True

        # heap_tight_edge에서 최소 시간 이벤트를 처리
        while not self.PriorityQueue.empty() and self.PriorityQueue.min().time == self.current_time:
            edge_id = self.PriorityQueue.min().to
            x, y = self.PriorityQueue.min().frm, self.edges[edge_id].to
            self.PriorityQueue.pop()
            if self.surface[x] == self.surface[y]:
                continue
            self.contract(x, y, edge_id)

        # heap_node_potential에서 최소 시간 이벤트를 처리
        while not self.BinaryHeap_int.empty() and self.BinaryHeap_int.min() == self.current_time:
            b = self.BinaryHeap_int.argmin()
            self.BinaryHeap_int.pop()
            self.expand(b)

        return False  # 증가 경로를 찾지 못했음을 의미

    def initialize(self) -> None:
        """
        Matching Algorithm의 초기 설정을 수행하는 메서드입니다.
        """

        # 큐를 초기화합니다.
        self.queue = deque([])

        # 매칭 배열을 초기화합니다.
        self.mate = [0 for _ in range(self.S)]

        # 각 노드의 링크를 초기화합니다.
        self.link = [self.Link(0, 0) for _ in range(self.S)]

        # 각 노드의 상태를 초기화합니다.
        self.label = [self.K_FREE for _ in range(self.S)]

        # 각 노드의 기본값을 자신의 인덱스로 초기화합니다.
        self.base = list(range(self.S))

        # 각 노드의 표면 값을 자신의 인덱스로 초기화합니다.
        self.surface = list(range(self.S))

        # 각 노드의 잠재력을 초기화합니다.
        self.potential = [0 for _ in range(self.S)]

        # 각 노드를 Node 객체로 초기화합니다.
        self.node = list(map(self.Node, range(self.S)))

        # 사용되지 않은 블로섬 ID를 초기화합니다.
        self.unused_blossom_id = [self.N + self.B - i for i in range(self.B)]
        self.unused_blossom_id_index = self.B

        # 시간을 초기화합니다.
        self.reset_time()

        # 각 노드의 생성 시간을 초기화합니다.
        self.time_created = [0 for _ in range(self.S)]

        # 각 노드의 슬랙 값을 무한대로 초기화합니다.
        self.slack = [inf for _ in range(self.S)]

        # 각 노드의 최적 slack 값을 초기화합니다.
        self.best_from = [0 for _ in range(self.S)]

        # 각 노드의 무거운 블로섬 값을 초기화합니다.
        self.heavy = [0 for _ in range(self.S)]

        # 각 노드의 지연 값을 초기화합니다.
        self.lazy = [0 for _ in range(self.S)]

        # 각 노드의 그룹을 초기화합니다.
        self.group = list(range(self.S))
        
    def set_potential(self) -> None:
        """
        각 노드의 잠재력을 최대 비용의 절반 값으로 초기화합니다.
        
        초기화를 통해 각 노드의 이중 변수(dual variable)를 설정하고,
        슬랙(slack) 계산을 단순화하며, 효율적인 비용 관리와 최적화된 매칭을 위한
        탐색 공간을 줄입니다. 이 방법은 알고리즘의 효율성과 안정성을 높입니다.
        """
        for u in range(1, self.N + 1):
            max_cost = 0

            # 각 노드에 연결된 엣지의 최대 비용 탐색
            for eid in range(self.offset[u], self.offset[u + 1]):
                max_cost = max(max_cost, self.edges[eid].cost)

            # 잠재력은 최대 비용의 절반으로 설정
            self.potential[u] = max_cost >> 1