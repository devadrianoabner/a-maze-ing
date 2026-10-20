from enum import IntFlag
from typing import Tuple, List


class Wall(IntFlag):
    N = 1  # 0001 North
    E = 2  # 0010 East
    S = 4  # 0100 South
    W = 8  # 1000 West
    ALL = 15  # 1111, all walls standing

    @property
    def opposite(self) -> "Wall":
        """Wall on the other side of the same boundary"""
        if self in (Wall.N, Wall.E):
            return Wall(self << 2)
        return Wall(self >> 2)

    @property
    def delta(self) -> Tuple[int, int]:
        """Step (delta_x, delta_y) to the neighbour on this side"""
        if self == Wall.N:
            return (0, -1)
        if self == Wall.E:
            return (1, 0)
        if self == Wall.S:
            return (0, 1)
        if self == Wall.W:
            return (-1, 0)
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
                row.append(self.ALL)  # 15 = f in hexadecimal
            cells.append(row)
        return cells

    def is_inside(self, x: int, y: int) -> bool:
        """True if (x, y) is a coordinate that exists in the grid"""
        return 0 <= x < self.width and 0 <= y < self.height
