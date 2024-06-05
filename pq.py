from heapq import heappush, heappop
from typing import Callable

class PriorityQueue:
    """
    파이썬의 heapq 라이브러리를 활용하여 우선순위 큐를 구현하는 클래스입니다. 
    이 클래스는 키 함수를 기반으로 하는 우선순위에 따라 요소들을 정렬합니다.
    기본적으로 파이썬의 heapq는 최소 힙을 구현하므로, 최소값을 우선순위로 하는 큐를 생성합니다.
    사용자는 우선순위 결정 로직을 커스텀하게 조정할 수 있도록 key 매개변수를 제공할 수 있습니다.
    """
    
    def __init__(self, key: Callable = lambda x: x):
        """
        우선순위 큐를 초기화합니다.

        Args:
            key (Callable): 우선순위 결정을 위한 키 함수
        """

        # 실제 요소들이 힙 자료구조를 통해 저장될 리스트
        self.heap: list[int] = []

        # 요소 비교에 사용될 키 생성 함수
        self.key = key
    
    def push(self, x: int) -> None:
        """
        우선순위 큐에 새 요소를 추가합니다.
        heapq 자료구조를 사용하여 O(log n) 시간 안에 요소가 추가됩니다.
        
        Args:
            x (int): 큐에 추가될 정수 요소
        """

        # heapq 모듈은 최소 힙만을 지원하므로, (우선순위, 값) 튜플 형태로 요소를 추가합니다.
        heappush(self.heap, (self.key(x), x))
    
    def pop(self) -> int:
        """
        우선순위가 가장 높은 요소를 제거하고 반환합니다.
        O(log n) 시간 안에 이루어집니다.
        
        Returns:
            int: 큐에서 제거된 요소
        """

        # 힙에서 요소를 제거하고, 저장된 값 중 두 번째 요소(실제 값)를 반환합니다.
        return heappop(self.heap)[1]

    def __len__(self) -> int:
        """
        현재 큐의 길이(요소 수)를 반환합니다.
        
        Returns:
            int: 큐 내 요소의 개수
        """

        # 현재 힙에 저장된 요소의 수를 반환합니다.
        return len(self.heap)