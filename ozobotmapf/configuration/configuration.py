import logging
import math

from ozobotmapf.graphics.shapes import Point


class Configuration:
    """Class computes and stores required configuration parameters that will be used throughout the application.

    Attributes:
        map_path (str): Path to the level file
        solver_path (str): Path to the solver executable
        fullscreen (bool): Flag if fullscreen mode is on
        window_width (int): Width of the window in pixels
        window_height (int): Height of the window in pixels
        mm_to_px (float): Conversion ratio between millimeters and pixels computed from display's DPI
        tile_size (int): Length of the tile's side in pixels
        tile_border_width (int): Width of the tile line in pixels
        line_width (int): Width of the following line in pixels
        wall_width (int): Width of the wall line in pixels
        color_code_radius (int): Radius of the flashing color code circle
        intersection_width (int): Length of the intersection indicator line
        max_map_width (int): Maximal level width in tiles
        max_map_height (int): Maximal level height in tiles
        top_margin (int): Distance between top of the window and top of the level in pixels
        left_margin (int): Distance between left border of the window and left border of the level in pixels
        map_origin (Point): Top-left point of the level
        map_width (int): Width of the level in tiles
        map_height (int): Height of the level in tiles
        map_agent_count (int): Number of agents on the level
        editor (bool): Flag if map editor mode is on
        display_grid (bool): Flag if tile grid should be displayed
        display_walls (bool): Flag if walls should be displayed
        agent_class (class): Class of the agents that should be initialized
        direction_preview (bool): Flag if direction preview arrow should be displayed before simulation
        step_time (int): Time that takes animated path to move between two tiles in milliseconds
        tail_lag (int): Time lag between the head and tail of the animated path in milliseconds
        colors (bool): Flag if OzobotAgent should use colored paths
    """

    def __init__(self, cli, config):
        """Initialization of Configuration from parsed command-line arguments and configuration file.

        Args:
            cli (namespace): Parsed command-line arguments
            config (dict[str, dict[str, float]): Parsed configuration file
        """
        self.map_path = None
        self.solver_path = None

        self.fullscreen = cli.fullscreen
        if self.fullscreen:
            self.window_width = config["display"]["resolution_width"]
            self.window_height = config["display"]["resolution_height"]
        else:
            self.window_width = cli.resolution[0]
            self.window_height = cli.resolution[1]

        self.mm_to_px = \
            ((config["display"]["resolution_width"] / config["display"]["display_width"]) +
             (config["display"]["resolution_height"] / config["display"]["display_height"])) / 2

        self.tile_size = round(config["ozobot"]["tile_size"] * self.mm_to_px)
        self.tile_border_width = math.floor(config["ozobot"]["tile_border_width"] * self.mm_to_px)
        self.line_width = round(config["ozobot"]["line_width"] * self.mm_to_px)
        self.wall_width = round(config["ozobot"]["wall_width"] * self.mm_to_px)
        self.color_code_radius = None
        self.intersection_width = None

        self.max_map_width = math.floor(self.window_width / self.tile_size)
        self.max_map_height = math.floor(self.window_height / self.tile_size)

        self.top_margin = math.floor((self.window_height - (self.tile_size * self.max_map_height)) / 2)
        self.left_margin = math.floor((self.window_width - (self.tile_size * self.max_map_width)) / 2)

        self.map_origin = Point(self.left_margin, self.top_margin)
        self.map_width, self.map_height, self.map_agent_count = [None] * 3

        self.editor = cli.editor

        self.display_grid = None
        self.display_walls = None
        self.agent_class = None
        self.direction_preview = None
        self.step_time = None
        self.tail_lag = None
        self.colors = None

    def __str__(self):
        return "CONFIGURATION PARAMETERS:\n" \
               "Map path: '{}'\n" \
               "Solver path: '{}'\n" \
               "Fullscreen: '{}'\n" \
               "Window width: {}px\n" \
               "Window height: {}px\n" \
               "Millimeter to pixels ratio: {:.3f}px\n" \
               "Tile size: {}px\n" \
               "Tile border width: {}px\n" \
               "Following line width: {}px\n" \
               "Wall line width: {}px\n" \
               "Color Code radius: {}px\n" \
               "Intersection indicator length: {}px\n" \
               "Max level width: {}\n" \
               "Max level height: {}\n" \
               "Top margin: {}px\n" \
               "Left margin: {}px\n" \
               "Map Origin: [{}, {}]\n" \
               "Map Attributes: [W: {}, H: {}, A: {}]\n" \
               "Map Editor mode: '{}'".format(
            self.map_path, self.solver_path, self.fullscreen, self.window_width, self.window_height, self.mm_to_px,
            self.tile_size, self.tile_border_width, self.line_width, self.wall_width, self.color_code_radius,
            self.intersection_width, self.max_map_width, self.max_map_height, self.top_margin, self.left_margin,
            self.map_origin[0], self.map_origin[1], self.map_width, self.map_height, self.map_agent_count, self.editor
        )


class SimulatorConfig(Configuration):
    """Simulator Configuration class."""

    def __init__(self, cli, config):
        """Initialization of Simulator Configuration from parsed command-line arguments and configuration file.

        Args:
            cli (namespace): Parsed command-line arguments
            config (dict[str, dict[str, float]): Parsed configuration file
        """
        super().__init__(cli, config)

        self.map_path = cli.map_file
        self.solver_path = config["solver"]["path"]
        self.map_width, self.map_height, self.map_agent_count = cli.map_attributes

        self.color_code_radius = round(config["ozobot"]["color_code_radius"] * self.mm_to_px)
        self.intersection_width = round(config["ozobot"]["intersection_width"] * self.mm_to_px)

        self.display_grid = config["simulator"]["display_borders"]
        self.display_walls = config["simulator"]["display_walls"]
        self.direction_preview = config["simulator"]["direction_preview"]
        self.agent_class = config["simulator"]["agent_type"]
        self.step_time = config["simulator"]["step_time"]
        self.tail_lag = config["simulator"]["tail_lag"]
        self.colors = config["simulator"]["colors"]

        logging.debug(str(self))


class EditorConfig(Configuration):
    """Map Editor Configuration class"""

    def __init__(self, cli, config):
        """Initialization of Map Editor Configuration from parsed command-line arguments and configuration file.

        Args:
            cli (namespace): Parsed command-line arguments
            config (dict[str, dict[str, float]): Parsed configuration file
        """
        super().__init__(cli, config)

        logging.debug(str(self))
