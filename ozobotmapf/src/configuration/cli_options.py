import logging
import os.path
import re

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
        logging.debug("Command-line arguments: {}".format(self.args))

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
        self.__parser.add_argument('-ma', '--map-attributes', nargs=3, type=int, dest='map_attributes',
                                   help='Map attributes: Width, height, number of agents.')
        self.__parser.add_argument('-d', '--debug', dest='debug', action='store_true',
                                   help='Log debugging messages.')

    def __validate_arguments(self):
        """Validates parsed command-line parameter values."""
        assert_argument(self.args.resolution[0] > 0, "Width resolution has to be > 0.")
        assert_argument(self.args.resolution[1] > 0, "Height resolution has to be > 0.")

        self.__validate_map()
        self.__validate_map_attributes()

    def __validate_map_attributes(self):
        """Method validates map attributes.

        Method checks if parameter -ma is used. It tries to get the attributes from map file name. If this fails,
        exception is thrown.
        """
        if self.args.map_attributes is None:
            numbers_in_name = [int(x) for x in re.findall(r'\d+', os.path.basename(self.args.map))]
            if len(numbers_in_name) < 3:
                assert_argument(False, "You have to define the map attributes with -ma parameter.")
            self.args.map_attributes = numbers_in_name[:3]
            logging.warning("You should use the `-ma` parameter to define map width, height and agent count. "
                            "This time first three numbers from the map file name were used as map attributes.")

    def __validate_map(self):
        """Method validates if the map command-line parameter contains a path to a valid file."""
        assert_argument(self.args.map is not None, "You have to provide a map.")
        if not os.path.isfile(self.args.map):
            if os.path.isfile("resources/maps/" + self.args.map):
                self.args.map = "resources/maps/" + self.args.map
            else:
                assert_argument(False, "Map has to be a path to a file or a map name from `resources/maps/` folder.")

