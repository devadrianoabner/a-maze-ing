"""The '42' pattern drawn with blocked cells."""
from typing import List, Set

from .board import Point

PATTERN_42: List[str] = [
    "X.X.XXX",
    "X.X...X",
    "XXX.XXX",
    "..X.X..",
    "..X.XXX",
]

MIN_WIDTH = 9
MIN_HEIGHT = 7


def pattern_42(width: int, height: int) -> Set[Point]:
    """Cells that draw a '42' in the center of a grid of this size.

    Returns an empty set (and prints an error) if the grid is too small.
    """
    if width < MIN_WIDTH or height < MIN_HEIGHT:
        print("Error: maze too small to draw the '42' pattern.")
        return set()

    pattern_height = len(PATTERN_42)
    pattern_width = len(PATTERN_42[0])
    offset_x = (width - pattern_width) // 2
    offset_y = (height - pattern_height) // 2

    blocked: Set[Point] = set()
    for row, line in enumerate(PATTERN_42):
        for column, char in enumerate(line):
            if char == "X":
                blocked.add(Point(offset_x + column, offset_y + row))
    return blocked
