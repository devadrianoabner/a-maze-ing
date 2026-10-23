from sys import argv

from config_loader import ConfigLoader, InputError, validate
from mazegen.menu import Menu


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
    Menu(config).run()


if __name__ == "__main__":
    main()
