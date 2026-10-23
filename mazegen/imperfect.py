import random
from typing import List, Set, Tuple
from .board import Grid, Point, Wall


def find_dead_ends(grid: Grid, blocked: Set[Point]) -> List[Point]:
    """Free cells that have exactly one open side."""
    dead_ends = []
    for y in range(grid.height):
        for x in range(grid.width):
            cell = Point(x, y)
            if cell in blocked:
                continue
            if grid.count_openings(cell) == 1:
                dead_ends.append(cell)
    return dead_ends


def _is_open_block(grid: Grid, corner: Point) -> bool:
    """True if the 3x3 block starting at corner has no inner walls."""
    for dy in range(3):
        for dx in range(3):
            cell = Point(corner.x + dx, corner.y + dy)
            if dx < 2 and Wall.E & grid.get_cell(cell):
                return False
            if dy < 2 and Wall.S & grid.get_cell(cell):
                return False
    return True


def _creates_open_area(grid: Grid, position: Point) -> bool:
    """True if some 3x3 block around the position is fully open."""
    for corner_y in range(position.y - 2, position.y + 1):
        for corner_x in range(position.x - 2, position.x + 1):
            corner = Point(corner_x, corner_y)
            fits_x = corner.x >= 0 and corner.x + 2 < grid.width
            fits_y = corner.y >= 0 and corner.y + 2 < grid.height
            if fits_x and fits_y and _is_open_block(grid, corner):
                return True
    return False


def remove_dead_ends(grid: Grid, blocked: Set[Point],
                     rng: random.Random) -> None:
    """Open a wall in each dead end, skipping openings that make a 3x3 area."""
    for dead_end in find_dead_ends(grid, blocked):
        if grid.count_openings(dead_end) != 1:
            continue
        options = _closed_neighbors(grid, dead_end, blocked)
        rng.shuffle(options)
        for wall, neighbour in options:
            grid.break_wall(dead_end, wall)
            area_here = _creates_open_area(grid, dead_end)
            area_there = _creates_open_area(grid, neighbour)
            if area_here or area_there:
                grid.build_wall(dead_end, wall)
            else:
                break


def _closed_neighbors(
    grid: Grid, cell: Point, blocked: Set[Point]
) -> List[Tuple[Wall, Point]]:
    """Neighbours behind a standing wall that are not blocked."""
    value = grid.get_cell(cell)
    options = []
    for wall, neighbour in grid.get_valid_neighbors(cell):
        if value & wall and neighbour not in blocked:
            options.append((wall, neighbour))
    return options
