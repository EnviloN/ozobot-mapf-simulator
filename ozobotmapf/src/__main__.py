import logging

from src.configuration.cli_options import CLIOptions
from src.configuration.config_options import ConfigOptions
from src.graphics.window import Window
from src.map.map import Map


def run_simulator():
    logging.info("Starting main process.")
    options = CLIOptions()
    args = options.args

    if args.debug:
        logging.getLogger().setLevel(logging.DEBUG)

    configurator = ConfigOptions('resources/config/monitor_config.ini')

    window = Window(args.resolution, args.fullscreen, configurator.config)
    map = Map(window.parameters)

    window.draw_tile_grid(map).update()


if __name__ == '__main__':
    logging.basicConfig(filename='resources/logs/log.log', format='%(asctime)s - %(levelname)s: %(message)s',
                        level=logging.INFO)
    run_simulator()
