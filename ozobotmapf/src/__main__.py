import logging

from src.configuration.cli_options import CLIOptions
from src.configuration.config_options import ConfigOptions
from src.graphics.display import Display


def run_simulator():
    logging.info("Starting main process.")
    options = CLIOptions()
    args = options.args

    if args.debug:
        logging.getLogger().setLevel(logging.DEBUG)

    configurator = ConfigOptions('resources/config/laptop_config.ini')
    display_config = configurator.display_config

    display = Display(args.resolution, args.fullscreen)


if __name__ == '__main__':
    logging.basicConfig(filename='resources/logs/log.log', format='%(levelname)s:%(message)s', level=logging.INFO)
    run_simulator()
