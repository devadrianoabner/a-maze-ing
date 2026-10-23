from typing import Dict, List, Set, Tuple

from .board import Grid, Point, Wall

WALL_CHAR = "█"
FREE_CHAR = " "
PATH_CHAR = "●"
CLOSED_CELL = 15  # all four walls standing: part of the '42'

ENTRY_COLOR = "\033[32m"  # green
EXIT_COLOR = "\033[31m"   # red
PATH_COLOR = "\033[96m"   # bright cyan
PATTERN_COLOR = "\033[38;5;208m"  # orange
FLOOR_BG = "\033[48;5;235m"  # dark gray background
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


def _between(first: Point, second: Point) -> Tile:
    """Canvas position of the passage between two neighbour cells."""
    return (first.x + second.x + 1, first.y + second.y + 1)


def _path_points(entry: Point, letters: str) -> List[Point]:
    """Cells visited when following the N/E/S/W letters from entry."""
    points = [entry]
    current = entry
    for letter in letters:
        step = Wall[letter].delta
        current = Point(current.x + step.x, current.y + step.y)
        points.append(current)
    return points


def _path_tiles(entry: Point, letters: str) -> Set[Tile]:
    """Canvas positions that the path goes through."""
    tiles: Set[Tile] = set()
    points = _path_points(entry, letters)
    for point in points:
        tiles.add(_tile(point))
    for current, following in zip(points, points[1:]):
        tiles.add(_between(current, following))
    return tiles


def _closed_cells(grid: Grid) -> Set[Point]:
    """Cells with all four walls standing (the '42')."""
    closed: Set[Point] = set()
    for y in range(grid.height):
        for x in range(grid.width):
            if grid.get_cell(Point(x, y)) == CLOSED_CELL:
                closed.add(Point(x, y))
    return closed


def _solid_colors(
    grid: Grid, entry: Point, exit_: Point
) -> Dict[Tile, str]:
    """Colour of the full blocks: the '42', the entry and the exit."""
    colors: Dict[Tile, str] = {}
    closed = _closed_cells(grid)
    for point in closed:
        colors[_tile(point)] = PATTERN_COLOR
        for wall in (Wall.E, Wall.S):
            step = wall.delta
            other = Point(point.x + step.x, point.y + step.y)
            if other in closed:
                colors[_between(point, other)] = PATTERN_COLOR
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
    solid = _solid_colors(grid, entry, exit_)
    path = _path_tiles(entry, letters)

    lines = []
    for row, chars in enumerate(canvas):
        line = ""
        for col, char in enumerate(chars):
            tile = (col, row)
            if tile in solid:
                line += solid[tile] + WALL_CHAR * 2 + RESET
            elif char == WALL_CHAR:
                line += wall_color + WALL_CHAR * 2 + RESET
            elif tile in path:
                line += FLOOR_BG + PATH_COLOR + PATH_CHAR + " " + RESET
            else:
                line += FLOOR_BG + "  " + RESET
        lines.append(line)
    return "\n".join(lines)
