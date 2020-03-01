import logging
import os.path
import re

from argparse import ArgumentParser
from ozobotmapf.configuration.config_exceptions import InvalidCLIOptionException
from ozobotmapf.utils.constants import Values


class CLIOptions:
    """Class handles parsing of command-line options.

    Attributes:
        __parser (ArgumentParser): Parser for command-line arguments
        args: Parsed arguments
    """

    def __init__(self):
        """Initialize CLIOptions instance

        Creates ArgumentParser and adds supported arguments.
        """
        self.__parser = ArgumentParser()
        self.__add_arguments()

        self.args = None

    def parse(self):
        """Method parses the command-line arguments.

        Returns:
            namespace: Parsed command-line arguments
        """
        self.args = self.__parser.parse_args()
        logging.debug("Command-line arguments: {}".format(self.args))

        self.__validate_arguments()
        logging.info("Command-line arguments parsed and validated.")

        return self.args

    def __add_arguments(self):
        """Adds supported parser arguments."""
        self.__parser.add_argument('-r', '--resolution', nargs=2, type=int, default=[1920, 1080], dest='resolution',
                                   help='Window resolution to be used [Width, Height].')
        self.__parser.add_argument('-f', '--full-screen', dest='fullscreen', action='store_true',
                                   help='Window is run in fullscreen mode.')
        self.__parser.add_argument('-m', '--level', type=str, dest='map_file',
                                   help='Map of the problem.')
        self.__parser.add_argument('-ma', '--level-attributes', nargs=3, type=int, dest='map_attributes',
                                   help='Map attributes: Width, height, number of agents.')
        self.__parser.add_argument('-d', '--debug', dest='debug', action='store_true',
                                   help='Log debugging messages.')
        self.__parser.add_argument('-c', '--config_file', type=str, dest='config_file',
                                   help='Application configuration file.')
        self.__parser.add_argument('-e', '--editor', dest='editor', action='store_true',
                                   help='Start level editor.')

    def __validate_arguments(self):
        """Validates parsed command-line parameter values."""
        assert_argument(self.args.resolution[0] > 0, "Width resolution has to be > 0.")
        assert_argument(self.args.resolution[1] > 0, "Height resolution has to be > 0.")

        if not self.args.editor:
            self.__validate_map()
            self.__validate_map_attributes()
        self.__validate_config_file()

    def __validate_map_attributes(self):
        """Method validates level attributes.

        Method checks if parameter -ma is used. It tries to get the attributes from level file name. If this fails,
        exception is thrown.
        """
        if self.args.map_attributes is None:
            numbers_in_name = [int(x) for x in re.findall(r'\d+', os.path.basename(self.args.map_file))]
            if len(numbers_in_name) < 3:
                assert_argument(False, "You have to define the level attributes with -ma parameter.")
            self.args.map_attributes = numbers_in_name[:3]
            logging.warning("You should use the `-ma` parameter to define level width, height and agent count. "
                            "This time first three numbers from the level file name were used as level attributes.")

    def __validate_map(self):
        """Method validates if the level command-line parameter contains a path to a valid file."""
        assert_argument(self.args.map_file is not None, "You have to provide a level.")
        if not os.path.isfile(self.args.map_file):
            if os.path.isfile(Values.MAPS_PATH + self.args.map_file):
                self.args.map_file = Values.MAPS_PATH + self.args.map_file
            else:
                assert_argument(False, "Map has to be a path to a file or a level name from `resources/maps/` folder.")

    def __validate_config_file(self):
        """Method validates if the config file command-line parameter contains a path to a valid file."""
        assert_argument(self.args.config_file is not None, "You have to provide a config file.")
        if not os.path.isfile(self.args.config_file):
            if os.path.isfile(Values.CONFIGS_PATH + self.args.config_file):
                self.args.config_file = Values.CONFIGS_PATH + self.args.config_file
            else:
                assert_argument(False, "Config file has to be a path to a file "
                                       "or a configuration name from `resources/configs/` folder.")
# ------------------------------------------------------------------------------------------------------------


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
