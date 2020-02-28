import logging
import os.path
from configparser import ConfigParser

from src.configuration.config_exceptions import InvalidConfigOptionException


class ConfigOptions:
    """Class handles parsing of a configuration file.

    Attributes:
        __raw_config (ConfigParser): Parser for configuration files
        config (dict[str, dict[str, float]): Parsed configuration file
    """

    def __init__(self, path):
        """Initialization of ConfigOptions instance.

        ConfigParser is initialized and reads the configuration file. Then it is parsed into a dictionary.

        Args:
            path (str): Path to the configuration file
        """
        self.__raw_config = ConfigParser(allow_no_value=True)
        self.__raw_config.read(path)

        self.config = None

    def parse(self):
        """Parses the raw config into a dict of dicts and validates the values.

        Each section of the configuration file is parsed separately into a dictionary.

        Note:
            Format: config['section']['option'] = value

        Returns:
            dict[str, dict[str, str]: Parsed configuration file
        """
        self.config = {}
        for section in self.__raw_config.sections():
            self.config[section] = self.__get_section_dict(section)

        self.__validate_config()
        logging.info("Config file parsed successfully: {}".format(self.config))

        return self.config

    def __get_section_dict(self, section):
        """Creates a dictionary from config file section.

        Args:
            section (str): Name of the configuration file section

        Returns:
            dict[str, str]: Parsed configuration file section
        """
        options = {}
        for option in self.__raw_config.options(section):
            options[option] = self.__raw_config.get(section, option)

        return options

    def __validate_config(self):
        """Validates the whole config file (with retyping).

        Each section is validated separately.
        """
        for section in self.config:
            if section == "solver":
                self.__validate_solver_section()
            else:
                self.__validate_section(section)

    def __validate_section(self, section):
        """Validates config section values.

        Values are retyped from str to float.

        Args:
            section (str): Name of the section

        Raises:
            ValueError: If value cannot be retyped to float or it is <= 0
        """
        for option in self.config[section]:
            try:
                self.config[section][option] = float(self.config[section][option])
                if self.config[section][option] <= 0:
                    raise ValueError
            except ValueError:
                raise_exception("'{}' option in '{}' section of the configuration file must be a positive number."
                                .format(option, section))

    def __validate_solver_section(self):
        """Method validates 'solver' section from configuration file."""
        if not os.path.isdir(self.config['solver']['path']):
            raise_exception("'path' option in 'solver' section must be a valid path to a directory.")


# ------------------------------------------------------------------------------------------------------------


def raise_exception(message):
    """Method logs the error and raises exception.

    Raises:
        InvalidConfigOptionException
    """
    logging.error(message)
    raise InvalidConfigOptionException(message)
