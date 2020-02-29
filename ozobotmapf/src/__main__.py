import logging
import pygame
from pygame.locals import *
import sys

from src.simulator.simulator import Simulator
from src.map_editor.editor import Editor
from src.configuration.configuration import SimulatorConfig, EditorConfig
from src.configuration.cli_options import CLIOptions
from src.configuration.config_options import ConfigOptions
from src.map.ozomap import OzoMap
from src.mapf_solvers.static_solvers import MapfSolverBoOX
from src.utils.constants import Values


def run_simulation(config):
    logging.info("Starting main simulation process.")

    ozomap = OzoMap(config).load_map(config)
    solver = init_solver(config)
    plans = solver.plan()

    window = Simulator(config)
    window.draw_map(ozomap).update()

    wait()

    for agent_id in plans:
        window.draw_full_path(
            ozomap.get_tiles_from_agent_positions(plans[agent_id]['pos_list'], False))
    window.update()

    wait()

    logging.info("Main simulation process finished successfully.")


def run_editor(config):
    logging.info("Starting main simulation process.")
    ozomap = OzoMap(config)

    editor = Editor(ozomap, config)
    editor.run()

    logging.info("Main simulation process finished successfully.")


def configure_application():
    """Function parses command-line arguments and configuration file, then creates an application configuration."""
    options = CLIOptions().parse()
    if not options.debug:
        logging.getLogger().setLevel(logging.INFO)

    config = ConfigOptions(options.config_file).parse()

    if options.editor:
        config_merge = EditorConfig(options, config)
    else:
        config_merge = SimulatorConfig(options, config)

    logging.info("Created the application configuration.")
    return config_merge


def init_solver(config):
    """Function initializes the solver instance with given arguments."""
    solver_args = {"input-file": config.map_path, "algorithm": "smtcbs++"}
    solver = MapfSolverBoOX(config.solver_path + "mapf_solver_boOX", solver_args)
    logging.info("Solver initialized.")
    return solver


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

    configuration = configure_application()
    if configuration.editor:
        run_editor(configuration)
    else:
        run_simulation(configuration)

    logging.info("----------------------------------------------------------------------------------------")
