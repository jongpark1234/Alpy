class Bulldozer:
    """Bulldozer-Trick(Rotating-Sweep-Line-Technique)을 구현한 클래스입니다."""

    class Point:
        """평면에서의 점을 나타내는 클래스입니다."""

        def __init__(self, x: int, y: int):
            self.x = x
            self.y = y
        
        def __lt__(self, other: 'Bulldozer.Point') -> bool:
            """
            두 점을 좌표를 기준으로 비교합니다.
            """
            return (self.x, self.y) < (other.x, other.y)

        def __eq__(self, other: 'Bulldozer.Point') -> bool:
            """
            두 점이 좌표 기준으로 동일한지 확인합니다.
            """
            return (self.x, self.y) == (other.x, other.y)

        @staticmethod
        def area(p1: 'Bulldozer.Point', p2: 'Bulldozer.Point', p3: 'Bulldozer.Point') -> int:
            """
            세 점으로 이루어진 삼각형의 면적을 계산하는 함수입니다.

            Args:
                p1 (Point): 첫 번째 점
                p2 (Point): 두 번째 점
                p3 (Point): 세 번째 점
            
            Returns:
                int: 세 점이 이루는 삼각형의 면적
            """
            return abs((p2.x - p1.x) * (p3.y - p2.y) - (p3.x - p2.x) * (p2.y - p1.y))

    class Line:
        """두 점 사이의 선분을 나타내는 클래스입니다."""

        def __init__(self, i: int, j: int, dx: int, dy: int):

            # 첫 번째 점, 두 번째 점의 인덱스
            self.i, self.j = i, j

            # x좌표, y좌표의 차
            self.dx, self.dy = dx, dy

        def __lt__(self, other: 'Bulldozer.Line') -> bool:
            """
            선분을 기울기를 기준으로 비교합니다.
            """
            return (self.dy * other.dx, self.i, self.j) < (other.dy * self.dx, other.i, other.j)

        def __eq__(self, other: 'Bulldozer.Line') -> bool:
            """
            두 선분이 기울기를 기준으로 동일한지 확인합니다.
            """
            return self.dy * other.dx == other.dy * self.dx

    def __init__(self, n: int):

        # 점의 개수
        self.size = n

        # 각 점의 현재 인덱스를 저장하는 리스트
        self.index = list(range(n))

        # 점 객체를 저장하는 리스트
        self.points: list[Bulldozer.Point] = []

        # 선 객체를 저장하는 리스트
        self.lines: list[Bulldozer.Line] = []

    def add_point(self, x: int, y: int):
        """
        평면상에 점을 추가합니다.

        Args:
            x (int): 추가될 점의 x좌표
            y (int): 추가될 점의 y좌표
        """
        self.points.append(self.Point(x, y))
    
    def rotate(self, pos: int):
        """
        주어진 선분의 인덱스를 기준으로 선분을 회전시킵니다.

        Args:
            pos (int): 회전할 선분의 인덱스
        """

        # 회전할 선분의 두 점의 인덱스
        x, y = self.lines[pos].i, self.lines[pos].j

        # 인덱스 배열을 사용하여 두 점 교환
        self.points[self.index[x]], self.points[self.index[y]] = self.points[self.index[y]], self.points[self.index[x]]

        # 두 점의 인덱스 교환
        self.index[x], self.index[y] = self.index[y], self.index[x]

    def set_up(self):
        """
        점을 정렬하고, 모든 점 쌍 사이의 선분을 생성하여 Bulldozer를 설정합니다.
        """

        # 점을 좌표 기준으로 정렬
        self.points.sort()

        # 모든 가능한 점 쌍 사이의 선분을 생성하고 정렬
        self.lines = sorted([
            self.Line(i, j, self.points[j].x - self.points[i].x, self.points[j].y - self.points[i].y) 
            for i in range(self.size) 
            for j in range(i + 1, self.size)
        ])