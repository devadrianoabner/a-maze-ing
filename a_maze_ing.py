from sys import argv


class InputError(Exception):
    def __init__(self, *args):
        super().__init__(*args)


def main():
    config = {}
    if len(argv) < 2:
        raise InputError("At least one argument is necessary")

    config_file = argv[1]
    try:
        with open(config_file, "r") as file:
            lines = file.read().splitlines()
            for line in lines:
                line = line.strip()
                if line.startswith("#"):
                    continue
                var = line.split("=")
                key, value = var[0].strip().lower(), var[1].strip()
                if value.find(",") > 0:
                    position = value.split(",")
                    if position[0].strip().isdigit():
                        position[0] = int(position[0])
                    else:
                        position[0] = -1
                    if position[1].strip().isdigit():
                        position[1] = int(position[1])
                    else:
                        position[1] = -1
                    value = tuple(position)
                elif value == "True" or value == "False":
                    value = value == "True"
                else:
                    if value.isdigit():
                        value = int(value)
                    else:
                        value = value.strip("\"\'")
                config[key] = value
    except FileNotFoundError:
        raise InputError("File doesn't exist")

    print(config)


if __name__ == "__main__":
    try:
        main()
    except InputError as error:
        print("InputError:", error)