from .board import Grid, Point, Wall

WALL_CHAR = "█"
FREE_CHAR = " "


def render(grid: Grid) -> str:
    """Draw the maze as text, walls as full blocks."""
    rows = []
    for y in range(grid.height):
        top = WALL_CHAR
        middle = WALL_CHAR
        for x in range(grid.width):
            cell = grid.get_cell(Point(x, y))
            top += WALL_CHAR if cell & Wall.N else FREE_CHAR
            top += WALL_CHAR
            middle += FREE_CHAR
            middle += WALL_CHAR if cell & Wall.E else FREE_CHAR
        rows.append(top)
        rows.append(middle)
    rows.append(WALL_CHAR * (2 * grid.width + 1))
    return "\n".join(rows)
