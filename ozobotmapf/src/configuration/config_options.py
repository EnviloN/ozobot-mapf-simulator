import logging
from configparser import ConfigParser

from src.configuration.config_exceptions import InvalidConfigOptionException


class ConfigOptions:
    """Class handles parsing of configuration files."""

    def __init__(self, path):
        """Creates a ConfigParser and parses a config file on given path."""
        self.config = ConfigParser(allow_no_value=True)
        self.config.read(path)

        self.display_config = self.get_section_dict("display")
        logging.info("Config file parsed successfully.")

    def get_section_dict(self, section):
        """Creates a dictionary from config file section."""
        options = {}
        for option in self.config.options(section):
            try:
                val = int(self.config.get(section, option))
                if val <= 0: raise ValueError
                options[option] = val
            except ValueError:
                message = "Dimensions and resolutions must be positive integers."
                logging.error("Config file parsing failed: {}".format(message))
                raise InvalidConfigOptionException(message)

        logging.debug("Display configuration: {}".format(options))
        return options
