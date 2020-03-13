import logging

from ozobotmapf.simulator.simulator import Simulator
from ozobotmapf.map_editor.editor import Editor
from ozobotmapf.configuration.configuration import EditorConfig, SimulatorConfig
from ozobotmapf.configuration.cli_options import CLIOptions
from ozobotmapf.configuration.config_options import ConfigOptions
from ozobotmapf.mapf_solvers.static_solvers import MapfSolverBoOX
from ozobotmapf.level.ozomap import OzoMap
from ozobotmapf.utils.constants import Values


def run_simulation(config):
    """Function runs the Simulator process

    Args:
        config (Configuration): Application configuration parameters
    """
    logging.info("Starting Simulator.")

    ozomap = OzoMap(config).load_map(config)
    solver = init_solver(config)
    plans = solver.plan()

    simulator = Simulator(ozomap, plans, config)
    simulator.run()

    logging.info("The Simulator finished successfully.")


def run_editor(config):
    """Function runs the Map Editor process

    Args:
        config (Configuration): Application configuration parameters
    """
    logging.info("Starting Map Editor.")
    ozomap = OzoMap(config)

    editor = Editor(ozomap, config)
    editor.run()

    logging.info("The Map Editor process finished.")


def configure_application():
    """Function parses command-line arguments and configuration file, then creates an application configuration."""
    options = CLIOptions().parse()
    if not options.debug:
        logging.getLogger().setLevel(logging.INFO)

    config = ConfigOptions(options.config_file).parse()
    config.update(ConfigOptions(Values.SIMULATOR_CONFIG).parse())

    if options.editor:
        config_merge = EditorConfig(options, config)
    else:
        config_merge = SimulatorConfig(options, config)

    logging.info("Created the application configuration.")
    return config_merge


def init_solver(config):
    """Function initializes the solver instance with given arguments."""
    # cbs, cbs+, cbs++, smtcbs, smtcbs+, smtcbs++
    solver_args = {"input-file": config.map_path, "algorithm": "smtcbs++"}
    solver = MapfSolverBoOX(config.solver_path + "mapf_solver_boOX", solver_args)
    logging.info("Solver initialized.")
    return solver


if __name__ == '__main__':
    logging.basicConfig(filename=Values.LOGS_PATH + "log.log", format='%(asctime)s - %(levelname)s: %(message)s',
                        level=logging.DEBUG)

    configuration = configure_application()
    if configuration.editor:
        run_editor(configuration)
    else:
        run_simulation(configuration)

    logging.info("----------------------------------------------------------------------------------------")
