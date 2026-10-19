from sys import argv
from config_loader import ConfigLoader, InputError


def main():
    if len(argv) < 2:
        print("Error: there must be at least one argument")
        return
    try:
        config = ConfigLoader("config.txt").load()
    except InputError as error:
        print("Error:", error)
        return
    print(config)


if __name__ == "__main__":
    main()
