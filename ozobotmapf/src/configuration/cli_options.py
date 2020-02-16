import logging

from argparse import ArgumentParser
from src.configuration.config_exceptions import InvalidCLIOptionException


def assert_argument(condition, message):
    """Function asserts the condition. If it is false, error is logged and exception raised."""
    if not condition:
        logging.error("Unsuccessful CLI option validation: {}".format(message))
        raise InvalidCLIOptionException(message)


class CLIOptions:
    """Class handles parsing of command-line options."""

    def __init__(self):
        """Creates an instance of CLIOptions and parses the command-line options."""
        self.parser = ArgumentParser()
        self.add_arguments()
        self.args = self.parser.parse_args()
        self.validate_arguments()
        logging.info("Command-line arguments parsed and validated.")

    def add_arguments(self):
        """Adds supported parser arguments."""
        self.parser.add_argument('-r', '--resolution', nargs=2, type=int, default=[1920, 1080], dest='resolution',
                                 help='Window resolution to be used [Width, Height].')
        self.parser.add_argument('-f', '--full-screen', dest='fullscreen', action='store_true',
                                 help='Window is run in fullscreen mode.')
        self.parser.add_argument('-d', '--debug', dest='debug', action='store_true',
                                 help='Log debugging messages.')

    def validate_arguments(self):
        """Validates parsed command-line parameter values."""
        assert_argument(self.args.resolution[0] > 0, "Width resolution has to be > 0.")
        assert_argument(self.args.resolution[1] > 0, "Height resolution has to be > 0.")

