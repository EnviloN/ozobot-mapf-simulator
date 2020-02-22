import logging
import os.path

from argparse import ArgumentParser
from src.configuration.config_exceptions import InvalidCLIOptionException


def assert_argument(condition, message):
    """Function asserts the condition.

    If the `condition` is false, error is logged and exception raised.

    Args:
          condition (bool)
          message (str): Message that is logged and passed to exception if condition does not hold

    Raises:
        InvalidCLIOptionException: If `condition` is false
    """
    if not condition:
        logging.error("Unsuccessful CLI option validation: {}".format(message))
        raise InvalidCLIOptionException(message)


class CLIOptions:
    """Class handles parsing of command-line options.

    Attributes:
        __parser (ArgumentParser): Parser for command-line arguments
        args: Parsed arguments
    """

    def __init__(self):
        """Initialize CLIOptions instance

        Creates ArgumentParser, adds supported arguments and parses the command-line arguments.
        """
        self.__parser = ArgumentParser()
        self.__add_arguments()

        self.args = self.__parser.parse_args()
        logging.info("Command-line arguments: {}".format(self.args))

        self.__validate_arguments()
        logging.info("Command-line arguments parsed and validated.")

    def __add_arguments(self):
        """Adds supported parser arguments."""
        self.__parser.add_argument('-r', '--resolution', nargs=2, type=int, default=[1920, 1080], dest='resolution',
                                   help='Window resolution to be used [Width, Height].')
        self.__parser.add_argument('-f', '--full-screen', dest='fullscreen', action='store_true',
                                   help='Window is run in fullscreen mode.')
        self.__parser.add_argument('-m', '--map', type=str, dest='map',
                                   help='Map of the problem.')
        self.__parser.add_argument('-d', '--debug', dest='debug', action='store_true',
                                   help='Log debugging messages.')

    def __validate_arguments(self):
        """Validates parsed command-line parameter values."""
        assert_argument(self.args.resolution[0] > 0, "Width resolution has to be > 0.")
        assert_argument(self.args.resolution[1] > 0, "Height resolution has to be > 0.")

        assert_argument(self.args.map is not None, "You have to provide a map.")
        if not os.path.isfile(self.args.map):
            if os.path.isfile("resources/maps/" + self.args.map):
                self.args.map = "resources/maps/" + self.args.map
            else:
                assert_argument(False, "Map has to be a path to a file or a map name from `resources/maps/` folder.")
