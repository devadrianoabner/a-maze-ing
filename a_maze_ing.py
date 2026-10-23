from sys import argv
from typing import Any, Dict
from mazegen.imperfect import remove_dead_ends

from config_loader import ConfigLoader, InputError, validate
from mazegen.board import Grid, Point
from mazegen.generator import MazeGenerator
from mazegen.pattern import pattern_42
from mazegen.solver import place_endpoints, solve
from mazegen.writer import build_output, write_output


def run(config: Dict[str, Any]) -> None:
    """Generate the maze described by the config and save it."""
    width = config["width"]
    height = config["height"]
    grid = Grid(width, height)
    blocked = pattern_42(width, height)

    entry = Point(*config["entry"])
    exit_ = Point(*config["exit"])
    entry, exit_ = place_endpoints(grid, entry, exit_, blocked)

    generator = MazeGenerator(grid, config.get("seed"), blocked)
    generator.generate()

    if not config["perfect"]:
        remove_dead_ends(grid, blocked, generator.rng)

    path = solve(grid, entry, exit_)
    text = build_output(grid, entry, exit_, path)
    write_output(text, config["output_file"])


def main() -> None:
    if len(argv) != 2:
        print("Usage: python3 a_maze_ing.py config.txt")
        return
    try:
        config = ConfigLoader(argv[1]).load()
        validate(config)
    except InputError as error:
        print("Error:", error)
        return
    run(config)


if __name__ == "__main__":
    main()
