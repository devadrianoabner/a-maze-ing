from sys import argv
from config_loader import ConfigLoader, InputError


def main() -> None:
    if len(argv) != 2:
        print("Usage: python3 a_maze_ing.py config.txt")
        return
    try:
        config = ConfigLoader(argv[1]).load()
    except InputError as error:
        print("Error:", error)
        return
    print(config)


if __name__ == "__main__":
    main()
