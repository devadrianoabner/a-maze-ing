from typing import Dict, List, Tuple

from .board import Grid, Point, Wall

WALL_CHAR = "█"
FREE_CHAR = " "
ENTRY_COLOR = "\033[32m"  # green
EXIT_COLOR = "\033[31m"   # red
PATH_COLOR = "\033[36m"   # cyan
RESET = "\033[0m"

WALL_COLORS = [
    "\033[37m",  # white
    "\033[33m",  # yellow
    "\033[35m",  # magenta
    "\033[34m",  # blue
]

Tile = Tuple[int, int]


def _carve(grid: Grid) -> List[List[str]]:
    """Canvas full of walls, with the open cells and passages carved."""
    canvas = []
    for _ in range(2 * grid.height + 1):
        canvas.append([WALL_CHAR] * (2 * grid.width + 1))

    for y in range(grid.height):
        for x in range(grid.width):
            cell = grid.get_cell(Point(x, y))
            col = 2 * x + 1
            row = 2 * y + 1
            canvas[row][col] = FREE_CHAR
            if not cell & Wall.N:
                canvas[row - 1][col] = FREE_CHAR
            if not cell & Wall.W:
                canvas[row][col - 1] = FREE_CHAR
    return canvas


def _tile(point: Point) -> Tile:
    """Canvas position (column, row) of the center of a cell."""
    return (2 * point.x + 1, 2 * point.y + 1)


def _path_points(entry: Point, letters: str) -> List[Point]:
    """Cells visited when following the N/E/S/W letters from entry."""
    points = [entry]
    current = entry
    for letter in letters:
        step = Wall[letter].delta
        current = Point(current.x + step.x, current.y + step.y)
        points.append(current)
    return points


def _colors(entry: Point, exit_: Point, letters: str) -> Dict[Tile, str]:
    """Color of each canvas position that is not plain wall or floor."""
    colors: Dict[Tile, str] = {}
    points = _path_points(entry, letters)
    for point in points:
        colors[_tile(point)] = PATH_COLOR
    for current, following in zip(points, points[1:]):
        middle = (current.x + following.x + 1, current.y + following.y + 1)
        colors[middle] = PATH_COLOR
    colors[_tile(entry)] = ENTRY_COLOR
    colors[_tile(exit_)] = EXIT_COLOR
    return colors


def render(
    grid: Grid,
    entry: Point,
    exit_: Point,
    letters: str = "",
    wall_color: str = WALL_COLORS[0],
) -> str:
    """Draw the maze as text. Pass the path letters to show the path."""
    canvas = _carve(grid)
    colors = _colors(entry, exit_, letters)

    lines = []
    for row, chars in enumerate(canvas):
        line = ""
        for col, char in enumerate(chars):
            color = colors.get((col, row))
            if color:
                line += color + WALL_CHAR + RESET
            elif char == WALL_CHAR:
                line += wall_color + char + RESET
            else:
                line += char
        lines.append(line)
    return "\n".join(lines)
