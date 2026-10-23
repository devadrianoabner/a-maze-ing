import random
from typing import Optional, Set, Tuple, List
from .board import Grid, Point, Wall


class MazeGenerator:
    def __init__(self, grid: Grid,
                 seed: Optional[int] = None,
                 blocked: Optional[Set[Point]] = None,
                 ) -> None:
        self.grid = grid
        self._rng = random.Random(seed)
        self._blocked: Set[Point] = blocked or set()
        self._visited: Set[Point] = set(self._blocked)

    @property
    def rng(self) -> random.Random:
        """Random generator shared with the imperfect step."""
        return self._rng

    def generate(self) -> None:
        """Carve a perfect maze into the grid."""
        start = self._pick_start()
        self._visited.add(start)
        active = [start]

        while active:
            index = self._rng.randrange(len(active))
            current = active[index]
            candidates = self._unvisited_neighbors(current)

            if candidates:
                wall, neighbour = self._rng.choice(candidates)
                self.grid.break_wall(current, wall)
                self._visited.add(neighbour)
                active.append(neighbour)
            else:
                active.pop(index)

    def _unvisited_neighbors(self, cell: Point) -> List[Tuple[Wall, Point]]:
        """Neighbours of the cell that are not part of the maze yet."""
        candidates = []
        neighbors = self.grid.get_valid_neighbors(cell)
        for wall, neighbour in neighbors:
            if neighbour not in self._visited:
                candidates.append((wall, neighbour))
        return candidates

    def _pick_start(self) -> Point:
        """Random free cell where the growth begins."""
        while True:
            x = self._rng.randint(0, self.grid.width - 1)
            y = self._rng.randint(0, self.grid.height - 1)
            start = Point(x, y)
            if start not in self._blocked:
                return start
