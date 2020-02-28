import logging
import pygame
from pygame.locals import *
import sys

from src.mapf_solvers.static_solvers import MapfSolverBoOX
from src.configuration.cli_options import CLIOptions
from src.configuration.config_options import ConfigOptions
from src.configuration.configuration import Configuration
from src.graphics.window import Window
from src.map.ozomap import OzoMap
from src.utils.constants import Values


def run_application():
    logging.info("Starting main process.")

    config = configure_application()

    ozomap = OzoMap(config).load_map(config)
    solver = init_solver(config)
    plans = solver.plan()

    window = Window(config)
    window.draw_map(ozomap).update()

    wait()

    for agent_id in plans:
        window.draw_full_path(
            ozomap.get_tiles_from_agent_positions(plans[agent_id]['pos_list'], False))
    window.update()

    wait()

    logging.info("Main process finished successfully.")


def configure_application():
    """Function parses command-line arguments and configuration file, then creates an application configuration."""
    options = CLIOptions().parse()
    if not options.debug:
        logging.getLogger().setLevel(logging.INFO)

    config = ConfigOptions(options.config_file).parse()

    configuration = Configuration(options, config)
    return configuration


def init_solver(config):
    solver_args = {"input-file": config.map_path, "algorithm": "smtcbs++"}
    return MapfSolverBoOX(config.solver_path + "mapf_solver_boOX", solver_args)


def wait():
    # TODO: Delete me when I'm not needed anymore.
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                logging.info("Quitting application.")
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:  # and event.key == K_ESCAPE:
                return


if __name__ == '__main__':
    logging.basicConfig(filename=Values.LOGS_PATH+"log.log", format='%(asctime)s - %(levelname)s: %(message)s',
                        level=logging.DEBUG)
    run_application()
    logging.info("----------------------------------------------------------------------------------------")
