import logging
import subprocess
import re

from ozobotmapf.mapf_solvers.solver import Solver
from ozobotmapf.mapf_solvers.solver_exception import SubprocessSolverException


class SubprocessSolver(Solver):
    """Abstract class for all external solvers that needs to be run as a subprocess.

    Note:
        The args attribute also contains a path to a level.

    Attributes:
        solver_path (str): Path to the solver file that is an executable
        args (dict[str, str]): Dictionary of all command-line arguments
    """

    def __init__(self, solver_path, args):
        """Initialize SubprocessSolver instance.

        Args:
            solver_path (str): Path to the solver file that is an executable
            args (dict[str, str]): Dictionary of all command-line arguments
        """
        self.solver_path = solver_path
        self.args = args

    def plan(self):
        """Abstract plan method."""
        pass

    def _build_arguments_string(self):
        """Method builds the argument list from the `args` attribute.

        Returns:
            list[str] - List of formatted command-line arguments for the subprocess
        """
        arg_str = []
        for arg in self.args:
            arg_str.append("--{}={}".format(arg, self.args[arg]))

        return arg_str


class MapfSolverBoOX(SubprocessSolver):
    """Class for the mapf_solver_boOX.

    Note:
        The args attribute also contains a path to a level.

    Attributes:
        solver (str): Path to the solver file that is an executable
        args (dict[str, str]): Dictionary of all command-line arguments
    """

    def __init__(self, solver, args):
        """Initialize the MapfSolverBoOX instance.

        Args:
            solver (str): Path to the solver file that is an executable
            args (dict[str, str]): Dictionary of all command-line arguments
        """
        super(MapfSolverBoOX, self).__init__(solver, args)

    def plan(self):
        """Method performs the planning and returns a plan.

        The method runs the solver subprocess and then parses its output.

        Returns:
            dict[int, dict[str, list]]: Parsed plans for every agent, including the list of positions and list of moves
        """
        output = self.__run_subprocess()
        return self.__parse_plan(str(output).replace('\\n', '\n'))

    def __run_subprocess(self):
        """Method runs the subprocess with all arguments.

        Returns:
            bytes: Output of the subprocess

        Raises:
            SubprocessSolverException: If the subprocess finishes with exit code other than 0
        """
        cmd = self.__build_subprocess_command()

        logging.info("Starting process: '{}'".format(" ".join(cmd)))
        process = subprocess.Popen(cmd, stdout=subprocess.PIPE)
        (output, err) = process.communicate()
        exit_code = process.wait()

        if exit_code:
            logging.error("Subprocess finished with exit code {}".format(exit_code))
            logging.error("ErrOut: {}".format(err))
            raise SubprocessSolverException("Subprocess finished with exit code {}".format(exit_code))

        logging.info("Subprocess finished successfully.")
        return output

    def __build_subprocess_command(self):
        """Method builds the command list for the subprocess module.

        Returns:
            list[str]: Command list including path to executable and command-line arguments.
        """
        return [self.solver_path, *self._build_arguments_string()]

    @staticmethod
    def __parse_plan(output):
        """Method parses the output string of the solver subprocess.

        Args:
            output (str): Output of the subprocess

        Returns:
            dict[int, dict[str, list]]: Parsed plans for every agent, including the list of positions and list of moves
        """
        agent_positions = [(int(aID), list(map(int, positions.split(' '))))
                           for aID, positions in re.findall(r"Agent (\d+): (.+)\n", output)]
        steps = [re.findall(r"(\d+)#(\d+)->(\d+)", x) for x in re.findall(r"Step \d+: (.*) \n", output)]
        steps = [[(int(x), int(y), int(z)) for x, y, z in step] for step in steps]

        agents = {}
        for aID, positions in agent_positions:
            agents[aID] = {'pos_list': positions, 'steps': []}
            for step in steps:
                moved = False
                for agent_step in step:
                    if aID == agent_step[0]:
                        agents[aID]['steps'].append((agent_step[1], agent_step[2]))
                        moved = True
                        break
                if not moved:
                    agents[aID]['steps'].append(None)

        logging.debug("Parsed agent plans: {}".format(agents))
        return agents
