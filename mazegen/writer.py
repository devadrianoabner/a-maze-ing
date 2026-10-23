from .board import Grid, Point


def build_output(
    grid: Grid, entry: Point, exit_: Point, path: str
) -> str:
    """Text of the output file: hex rows, blank line, entry, exit, path."""
    lines = []
    for y in range(grid.height):
        row = ""
        for x in range(grid.width):
            row += format(grid.get_cell(Point(x, y)), "X")
        lines.append(row)

    lines.append("")
    lines.append(f"{entry.x},{entry.y}")
    lines.append(f"{exit_.x},{exit_.y}")
    lines.append(path)
    return "\n".join(lines) + "\n"


def write_output(text: str, filename: str) -> bool:
    """Save the text. Returns False and prints an error on failure."""
    try:
        with open(filename, "w") as file:
            file.write(text)
    except OSError as error:
        print(f"Error: could not write '{filename}': {error}")
        return False
    return True
