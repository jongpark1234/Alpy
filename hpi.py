from math import hypot
from collections import deque

class Point:
    def __init__(self, x: int = 0, y: int = 0):
        self.x = x
        self.y = y

class Line:
    """
    ax + by = c
    """
    def __init__(self, a: int, b: int, c: int):
        self.a = a
        self.b = b
        self.c = c
    
    def slope(self) -> Point:
        return Point(self.a, self.b)

    def __lt__(self, other: 'Line') -> bool:
        f1 = (self.a, self.b) > (0, 0)
        f2 = (other.a, other.b) > (0, 0)
        if f1 != f2:
            return f1 > f2
        t = HalfPlaneIntersection.ccw(Point(), self.slope(), other.slope())
        return self.c * hypot(other.a, other.b) < other.c * hypot(self.a, self.b) if t == 0 else t > 0

class HalfPlaneIntersection:
    """
    반평면 교집합을 처리하는 클래스입니다.
    """

    @staticmethod
    def ccw(p1: Point, p2: Point, p3: Point) -> float:
        """
        반시계 방향 여부를 판단합니다. (ccw)

        Args:
            p1 (Point): 첫 번째 점
            p2 (Point): 두 번째 점
            p3 (Point): 세 번째 점

        Returns:
            float: 세 점의 ccw (+: 반시계, -: 시계, 0: 일직선)
        """
        return (p2.x - p1.x) * (p3.y - p1.y) - (p2.y - p1.y) * (p3.x - p1.x)
    
    def intersect(self, a: Line, b: Line) -> tuple[float]:
        """
        두 선분의 교점을 구합니다.

        Args:
            a (Line): 첫 번째 선분
            b (Line): 두 번째 선분
        
        Returns:
            tuple[float]: 교점을 나타내는 튜플 (x, y)
        """
        det = a.a * b.b - b.a * a.b
        return ((a.c * b.b - a.b * b.c) / det, (a.a * b.c - a.c * b.a) / det)

    def bad(self, a: Line, b: Line, c: Line) -> bool:
        """
        교점이 교집합을 이루지 않는지 여부를 판단하여 반환합니다.

        Args:
            a (Line): 첫 번째 선분
            b (Line): 두 번째 선분
            c (Line): 세 번째 선분

        Returns:
            bool: 교집합을 이루지 않으면 True, 그렇지 않으면 False
        """

        # 첫 번째 선분과 두 번째 선분의 기울기가 반시계 방향이 아니면 교점이 없음
        if self.ccw(Point(), a.slope(), b.slope()) <= 0:
            return False
        
        # 첫 번째 선분과 두 번째 선분의 교점을 구함
        cross = self.intersect(a, b)

        # 교점의 좌표가 세 번째 선분의 반평면에 포함되는지 확인
        return cross[0] * c.a + cross[1] * c.b >= c.c

    def process(self, lines: list[Line]) -> list[Point]:
        """
        반평면 교집합을 처리하여 결과를 반환합니다.

        Args:
            lines (list[Line]): 처리할 선분 리스트
        
        Returns:
            list[Point]: 교집합을 이루는 점들의 리스트
        """
        
        # 덱을 이용해 선분 관리
        dq: deque[Line] = deque([])
        
        # 결괏값을 반환할 리스트
        ret = []

        # 선분들을 기울기 기준으로 정렬
        lines.sort()
        
        # 모든 선분 탐색
        for line in lines:

            # 동일한 기울기의 선분 건너뛰기
            if dq and self.ccw(Point(), dq[-1].slope(), line.slope()) == 0:
                continue
            
            # 덱의 끝에서부터 나쁜 선분을 제거
            while len(dq) >= 2 and self.bad(dq[-2], dq[-1], line):
                dq.pop()
            
            # 덱의 앞에서부터 나쁜 선분을 제거
            while len(dq) >= 2 and self.bad(line, dq[0], dq[1]):
                dq.popleft()

            # 현재 선분을 덱에 추가
            dq.append(line)

        # 덱의 끝에서부터 나븐 선분을 제거        
        while len(dq) > 2 and self.bad(dq[-2], dq[-1], dq[0]):
            dq.pop()

        # 덱의 앞에서부터 나쁜 선분을 제거
        while len(dq) > 2 and self.bad(dq[-1], dq[0], dq[1]):
            dq.popleft()
        
        # 최종적으로 남은 선분들로 교점을 구함
        for i in range(len(dq)):
            cur, nxt = dq[i], dq[(i + 1) % len(dq)]

            # 두 선분이 반시계 방향이 아니면 빈 리스트 반환
            if self.ccw(Point(), cur.slope(), nxt.slope()) <= 0:
                return []

            # 두 선분의 교점을 리스트에 추가
            ret.append(self.intersect(cur, nxt))
        
        # 결괏값 반환
        return ret