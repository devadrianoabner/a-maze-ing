

class InputError(Exception):
    """Raised when the user input is wrong."""
    def __init__(self, *args):
        super().__init__(*args)


class ConfigLoader:
    def __init__(self, config_file: str):
        self.config_file = config_file

    def _value_cast(self, value: str) -> any:
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

    def load(self) -> dict:
        """Load the configuration file into a config dict."""
        config = {}
        try:
            with open(self.config_file, "r") as file:
                lines = file.read().splitlines()
        except FileNotFoundError:
            raise InputError(f"file {self.config_file} not found.")

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
