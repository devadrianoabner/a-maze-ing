import random
from typing import List, Tuple, Iterator

N: int = 1  # 0001
E: int = 2  # 0010
S: int = 4  # 0100
W: int = 8  # 1000

DIRECTION = {
    N: (0, -1),
    E: (1, 0),
    S: (0, 1),
    W: (-1, 0)
}


class Board:
    def __init__(self, width, height, start, end, seed: int = None):
        self.width = width
        self.height = height
        self.start = start
        self.end = end
        self.seed = seed
        self.board = [[15 for _ in range(width)] for _ in range(height)]
        self.visited = [[False for _ in range(width)] for _ in range(height)]
        self.possible: List[Tuple[int, int]] = []

    def _get_oposite_wall(self, wall: int) -> int:
        """Calculates the opposite wall based on the wall. ROFL"""
        if wall <= 2:
            return wall << 2
        else:
            return wall >> 2

    def _break_wall(self, x, y, wall):
        """Breaks a wall from x to an neighbour x."""
        self.board[y][x] &= ~wall

        opposite = self._get_oposite_wall(wall)

        dx, dy = DIRECTION[wall]
        nx, ny = x + dx, y + dy

        self.board[ny][nx] &= ~opposite

    def _get_valid_neighbors(self, x, y) -> Iterator[Tuple[int, int, int]]:
        """Test the important neighbours."""
        for wall, (dx, dy) in DIRECTION.items():
            nx, ny = x + dx, y + dy
            if 0 <= nx < self.width and 0 <= ny < self.height:
                yield wall, nx, ny

    def generate(self) -> None:
        """Generate a maze."""
        if self.seed is not None:
            random.seed(self.seed)

        sx, sy = random.randint(0, self.width - 1), random.randint(0, self.height - 1)
        self.visited[sy][sx] = True

        for wall, nx, ny in self._get_valid_neighbors(sx, sy):
            self.possible.append((nx, ny))

        while self.possible:
            idx = random.randint(0, len(self.possible) - 1)
            px, py = self.possible.pop(idx)
            
            if self.visited[py][px]:
                continue

            maze_neighbors = []
            for wall, nx, ny in self._get_valid_neighbors(px, py):
                if self.visited[ny][nx]:
                    maze_neighbors.append(wall)

            if maze_neighbors:
                wall_to_break = random.choice(maze_neighbors)
                self._break_wall(px, py, wall_to_break)

            self.visited[py][px] = True

            for wall, nx, ny in self._get_valid_neighbors(px, py):
                if not self.visited[ny][nx]:
                    self.possible.append((nx, ny))

    def print_maze_hex(self) -> None:
        """Print the maze in the hex specification."""
        for row in self.board:
            hex_row = "".join([hex(cell)[2:] for cell in row])
            print(hex_row)
