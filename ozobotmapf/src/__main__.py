import logging
import pygame
from pygame.locals import *
import sys

from src.algorighms.static_solvers import MapfSolverBoOX
from src.configuration.cli_options import CLIOptions
from src.configuration.config_options import ConfigOptions
from src.graphics.window import Window
from src.map.ozomap import OzoMap


def run_simulator():
    logging.info("Starting main process.")

    options = CLIOptions()
    args = options.args
    if not args.debug:
        logging.getLogger().setLevel(logging.INFO)

    configurator = ConfigOptions('resources/config/laptop_config.ini')

    window = Window(args.resolution, args.fullscreen, configurator.config)
    ozomap = OzoMap(window.parameters)

    solver_args = {"input-file": args.map, "algorithm": "smtcbs++"}
    solver = MapfSolverBoOX(configurator.config['solver']['path'] + "mapf_solver_boOX", solver_args)

    ozomap.load_map(args.map, args.map_attributes)
    window.draw_map(ozomap).update()

    plans = solver.plan()

    wait()

    for agent_id in plans:
        window.draw_full_path(
            ozomap.get_tiles_from_agent_positions(plans[agent_id]['pos_list'], False))
    window.update()

    wait()

    logging.info("Main process finished successfully.")


def wait():
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                logging.info("Quitting application.")
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:  # and event.key == K_ESCAPE:
                return


if __name__ == '__main__':
    logging.basicConfig(filename='resources/logs/log.log', format='%(asctime)s - %(levelname)s: %(message)s',
                        level=logging.DEBUG)
    run_simulator()
    logging.info("----------------------------------------------------------------------------------------")
