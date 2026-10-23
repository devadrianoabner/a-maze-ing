from typing import Any, Dict

from .board import Grid, Point
from .display import WALL_COLORS, render
from .generator import MazeGenerator
from .imperfect import remove_dead_ends
from .pattern import pattern_42
from .solver import place_endpoints, solve
from .writer import build_output, write_output


class Menu:
    def __init__(self, config: Dict[str, Any]) -> None:
        self.config = config
        self.seed = config.get("seed")
        self.show_path = False
        self.color_index = 0
        self.grid = Grid(config["width"], config["height"])
        self.entry = Point(0, 0)
        self.exit_ = Point(0, 0)
        self.letters = ""
        self.regenerate()

    def regenerate(self) -> None:
        """Build a new maze from the config, solve it and save it."""
        width = self.config["width"]
        height = self.config["height"]
        self.grid = Grid(width, height)
        blocked = pattern_42(width, height)

        entry = Point(*self.config["entry"])
        exit_ = Point(*self.config["exit"])
        self.entry, self.exit_ = place_endpoints(
            self.grid, entry, exit_, blocked
        )

        generator = MazeGenerator(self.grid, self.seed, blocked)
        generator.generate()
        if not self.config["perfect"]:
            remove_dead_ends(self.grid, blocked, generator.rng)
        self.seed = None
        self.letters = solve(self.grid, self.entry, self.exit_)

        text = build_output(self.grid, self.entry, self.exit_, self.letters)
        write_output(text, self.config["output_file"])

    def draw(self) -> None:
        """Clear the screen and draw the maze."""
        letters = self.letters if self.show_path else ""
        color = WALL_COLORS[self.color_index]
        print("\033[H\033[J", end="")
        print(render(self.grid, self.entry, self.exit_, letters, color))

    def toggle_path(self) -> None:
        """Show the path if hidden, hide it if shown."""
        self.show_path = not self.show_path

    def next_color(self) -> None:
        """Move to the next wall colour."""
        self.color_index = (self.color_index + 1) % len(WALL_COLORS)

    def run(self) -> None:
        """Show the menu until the user quits."""
        while True:
            self.draw()
            print("=== A-Maze-ing ===")
            print("1. Re-generate a new maze")
            print("2. Show / Hide the shortest path")
            print("3. Rotate the wall colours")
            print("4. Quit")
            try:
                choice = input("Choice? (1-4): ").strip()
            except (EOFError, KeyboardInterrupt):
                return
            if choice == "1":
                self.regenerate()
            elif choice == "2":
                self.toggle_path()
            elif choice == "3":
                self.next_color()
            elif choice == "4":
                return
