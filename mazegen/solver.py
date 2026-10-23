from collections import deque
from typing import Deque, Dict, Optional, List
from .board import Grid, Point, Wall


def _explore(grid: Grid, entry: Point) -> Dict[Point, Optional[Point]]:
    """Walk outward from entry, remembering where each cell came from."""
    came_from: Dict[Point, Optional[Point]] = {entry: None}
    queue: Deque[Point] = deque([entry])

    while queue:
        current = queue.popleft()
        for wall, neighbour in grid.get_open_neighbors(current):
            if neighbour not in came_from:
                came_from[neighbour] = current
                queue.append(neighbour)
    return came_from


def _trace_back(
    came_from: Dict[Point, Optional[Point]], exit_: Point
) -> List[Point]:
    """Follow the came_from map from exit back to entry."""
    path: List[Point] = []
    cell: Optional[Point] = exit_
    while cell is not None:
        path.append(cell)
        cell = came_from[cell]
    path.reverse()
    return path


def _to_letters(path: List[Point]) -> str:
    """Turn a list of cells into a string of N/E/S/W moves."""
    letters = ""
    for current, following in zip(path, path[1:]):
        step = Point(following.x - current.x, following.y - current.y)
        for wall in Wall:
            if wall.delta == step:
                letters += wall.name
    return letters


def solve(grid: Grid, entry: Point, exit_: Point) -> str:
    """Shortest path from entry to exit as a string of N/E/S/W."""
    came_from = _explore(grid, entry)
    path = _trace_back(came_from, exit_)
    return _to_letters(path)
