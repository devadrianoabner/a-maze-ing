from enum import IntFlag
from typing import List, NamedTuple, Tuple


class Point(NamedTuple):
    x: int
    y: int


class Wall(IntFlag):
    N = 1  # 0001 North
    E = 2  # 0010 East
    S = 4  # 0100 South
    W = 8  # 1000 West

    @property
    def opposite(self) -> "Wall":
        """Wall on the other side of the same boundary"""
        if self in (Wall.N, Wall.E):
            return Wall(self << 2)
        return Wall(self >> 2)

    @property
    def delta(self) -> Point:
        """Step to the neighbour on this side"""
        if self == Wall.N:
            return Point(0, -1)
        if self == Wall.E:
            return Point(1, 0)
        if self == Wall.S:
            return Point(0, 1)
        if self == Wall.W:
            return Point(-1, 0)
        raise ValueError(f"{self!r} is not a single direction")


class Grid:
    def __init__(self, width: int, height: int) -> None:
        self.width = width
        self.height = height
        self._cells = self._build_cells()

    def _build_cells(self) -> List[List[int]]:
        cells = []
        for _ in range(self.height):
            row = []
            for _ in range(self.width):
                row.append(15)  # 15 or f in hexadecimal
            cells.append(row)
        return cells

    def is_inside(self, position: Point) -> bool:
        """True if the position exists in the grid"""
        if position.x < 0 or position.x >= self.width:
            return False
        if position.y < 0 or position.y >= self.height:
            return False
        return True

    def get_cell(self, position: Point) -> int:
        """Value of the cell at (x, y)"""
        return self._cells[position.y][position.x]

    def break_wall(self, position: Point, wall: Wall) -> None:
        """Open the wall on the given side, in both neighbouring cells"""
        step = wall.delta
        neighbour = Point(position.x + step.x, position.y + step.y)

        self._cells[position.y][position.x] &= ~wall
        self._cells[neighbour.y][neighbour.x] &= ~wall.opposite

    def get_valid_neighbors(self, position: Point) -> List[Tuple[Wall, Point]]:
        """Sides of the position that have a neighbour inside the grid"""
        neighbors = []
        for wall in Wall:
            step = wall.delta
            neighbour = Point(position.x + step.x, position.y + step.y)
            if self.is_inside(neighbour):
                neighbors.append((wall, neighbour))
        return neighbors

    def get_open_neighbors(self, position: Point) -> List[Tuple[Wall, Point]]:
        """Neighbours reachable from the position without crossing a wall."""
        cell = self.get_cell(position)
        reachable = []
        for wall, neighbour in self.get_valid_neighbors(position):
            if not cell & wall:
                reachable.append((wall, neighbour))
        return reachable

    def count_openings(self, position: Point) -> int:
        """How many sides of the cell are open."""
        return len(self.get_open_neighbors(position))

    def build_wall(self, position: Point, wall: Wall) -> None:
        """Close the wall on the given side, in both neighbouring cells."""
        step = wall.delta
        neighbour = Point(position.x + step.x, position.y + step.y)

        self._cells[position.y][position.x] |= wall
        self._cells[neighbour.y][neighbour.x] |= wall.opposite
