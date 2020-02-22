import logging
import pygame
from pygame.locals import *
import sys

from src.configuration.cli_options import CLIOptions
from src.configuration.config_options import ConfigOptions
from src.graphics.window import Window
from src.map.ozomap import OzoMap


def run_simulator():
    logging.info("Starting main process.")
    options = CLIOptions()
    args = options.args

    if args.debug:
        logging.getLogger().setLevel(logging.DEBUG)

    configurator = ConfigOptions('resources/config/monitor_config.ini')

    window = Window(args.resolution, args.fullscreen, configurator.config)
    ozomap = OzoMap(window.parameters)

    ozomap.load_map(args.map)
    window.draw_map(ozomap).update()

    wait()

    logging.info("Stopping main process successfully.")


def wait():
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN and event.key == K_ESCAPE:
                return


if __name__ == '__main__':
    logging.basicConfig(filename='resources/logs/log.log', format='%(asctime)s - %(levelname)s: %(message)s',
                        level=logging.INFO)
    run_simulator()
