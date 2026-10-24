"""Read and validate the configuration file."""
from typing import Any, Dict


class InputError(Exception):
    """Raised when the user input is wrong."""


class ConfigLoader:
    """Read a KEY=VALUE configuration file into a dictionary."""
    def __init__(self, config_file: str) -> None:
        """Remember which file to read.

        Args:
            config_file: Path of the configuration file.
        """
        self.config_file = config_file

    def _value_cast(self, value: str) -> Any:
        """Cast the input to a supported value."""
        if value.isdigit():
            return int(value)
        elif "," in value:
            pos = value.split(",", 1)
            try:
                result = (int(pos[0].strip()), int(pos[1].strip()))
            except ValueError:
                raise InputError(f"invalid position: {value}")
            return result
        elif value == "True" or value == "False":
            return value == "True"
        else:
            return value.strip("'\"")

    def load(self) -> Dict[str, Any]:
        """Load the configuration file into a config dict."""
        config = {}
        try:
            with open(self.config_file, "r") as file:
                lines = file.read().splitlines()
        except OSError as error:
            raise InputError(f"cannot read {self.config_file}: {error}")

        for line in lines:
            line = line.strip()
            if not line or line.startswith("#"):
                continue

            var = line.split("=", 1)
            if len(var) != 2:
                continue

            key = var[0].strip().lower()
            value = var[1].strip()
            config[key] = self._value_cast(value)

        return config


REQUIRED_KEYS = ("width", "height", "entry", "exit", "output_file", "perfect")


def validate(config: Dict[str, Any]) -> None:
    """Check that the config can produce a valid maze.

    Args:
        config: The dictionary returned by ConfigLoader.load.

    Raises:
        InputError: If a key is missing, a value has the wrong type, a
            position is outside the maze, or entry equals exit.
    """
    for key in REQUIRED_KEYS:
        if key not in config:
            raise InputError(f"missing key: {key.upper()}")

    width, height = config["width"], config["height"]
    if not isinstance(config["perfect"], bool):
        raise InputError("PERFECT must be True or False")
    if not isinstance(width, int) or not isinstance(height, int):
        raise InputError("WIDTH and HEIGHT must be integers")
    if width < 1 or height < 1:
        raise InputError("WIDTH and HEIGHT must be positive")
    if not isinstance(config["perfect"], bool):
        raise InputError("PERFECT must be True or False")

    seed = config.get("seed")
    if seed is not None and not isinstance(seed, int):
        raise InputError("SEED must be an integer")

    for key in ("entry", "exit"):
        value = config[key]
        if not isinstance(value, tuple):
            raise InputError(f"{key.upper()} must be x,y")
        x, y = value
        if not (0 <= x < width and 0 <= y < height):
            raise InputError(f"{key.upper()} is outside the maze")

    if config["entry"] == config["exit"]:
        raise InputError("ENTRY and EXIT must be different")
