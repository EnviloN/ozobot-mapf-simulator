import logging
from configparser import ConfigParser

from src.configuration.config_exceptions import InvalidConfigOptionException


class ConfigOptions:
    """Class handles parsing of configuration files."""

    def __init__(self, path):
        """Creates a ConfigParser and parses a config file on given path."""
        self.raw_config = ConfigParser(allow_no_value=True)
        self.raw_config.read(path)

        self.config = self.parse()
        self.validate_config()

        logging.info("Config file parsed successfully: {}".format(self.config))

    def parse(self):
        """Parses the raw config into a dict of dicts.

        Format: config['section']['option']
        """
        config = {}
        for section in self.raw_config.sections():
            config[section] = self.get_section_dict(section)

        return config

    def get_section_dict(self, section):
        """Creates a dictionary from config file section."""
        options = {}
        for option in self.raw_config.options(section):
            options[option] = self.raw_config.get(section, option)

        return options

    def validate_config(self):
        """Validates the whole config file (with retyping)."""
        for section in self.config:
            self.validate_section(section)

    def validate_section(self, section):
        """Validates config section values."""
        for option in self.config[section]:
            try:
                self.config[section][option] = float(self.config[section][option])
                if self.config[section][option] <= 0:
                    raise ValueError
            except ValueError:
                raise InvalidConfigOptionException(
                    "'{}' option in '{}' section of the configuration file must be a positive number."
                    .format(option, section)
                )
