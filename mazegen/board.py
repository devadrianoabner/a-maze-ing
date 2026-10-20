from enum import IntFlag
from typing import Tuple


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
