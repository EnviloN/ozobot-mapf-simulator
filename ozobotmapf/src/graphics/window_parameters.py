import logging
import math

from src.graphics.point import Point


class WindowParameters:
    """Class computes and stores all display and rendering parameters.

    Attributes:
        window_width (int): Width of the window in pixels
        window_height (int): Height of the window in pixels
        display_width (int): Width of the display in pixels
        display_height (int): Height of the display in pixels
        mm_to_px (float): Conversion ratio between millimeters and pixels computed from display's DPI
        tile_size (int): Length of the tile's side in pixels
        tile_line_width (int): Width of the tile line in pixels
        line_width (int): Width of the following line in pixels
        wall_width (int): Width of the wall line in pixels
        max_map_width (int): Maximal map width in tiles
        max_map_height (int): Maximal map height in tiles
        top_margin (int): Distance between top of the window and top of the map in pixels
        left_margin (int): Distance between left border of the window and left border of the map in pixels
        origin (Point): Top-left point of the map
    """

    def __init__(self, resolution, config):
        """Initialization of WindowParameters from parsed config file.

        Args:
            resolution (list[int]): Width and height of the application window
            config (dict[str, dict[str, float]): Parsed configuration file
        """
        self.window_width = int(resolution[0])
        self.window_height = int(resolution[1])
        self.display_width = int(config["display"]["resolution_width"])
        self.display_height = int(config["display"]["resolution_height"])

        self.mm_to_px = \
            ((config["display"]["resolution_width"] / config["display"]["display_width"]) +
             (config["display"]["resolution_height"] / config["display"]["display_height"])) / 2

        self.tile_size = round(config["ozobot"]["tile_size"] * self.mm_to_px)
        self.tile_line_width = math.floor(config["ozobot"]["tile_line_width"] * self.mm_to_px)
        self.line_width = round(config["ozobot"]["line_width"] * self.mm_to_px)
        self.wall_width = round(config["ozobot"]["wall_width"] * self.mm_to_px)

        self.max_map_width = math.floor(self.window_width / self.tile_size)
        self.max_map_height = math.floor(self.window_height / self.tile_size)

        self.top_margin = math.floor((self.window_height - (self.tile_size * self.max_map_height)) / 2)
        self.left_margin = math.floor((self.window_width - (self.tile_size * self.max_map_width)) / 2)

        self.origin = Point(self.left_margin, self.top_margin)

        logging.debug(str(self))

    def __str__(self):
        return "DISPLAY PARAMETERS:\n" \
               "Window width: {}px\n" \
               "Window height: {}px\n" \
               "Display width: {}px\n" \
               "Display height: {}px\n" \
               "Millimeter to pixels ratio: {:.3f}px\n" \
               "Tile size: {}px\n" \
               "Tile line width: {}px\n" \
               "Following line width: {}px\n" \
               "Wall line width: {}px\n" \
               "Max map width: {}\n" \
               "Max map height: {}\n" \
               "Top margin: {}px\n" \
               "Left margin: {}px\n" \
               "Map Origin: [{}, {}]".format(
            self.window_width, self.window_height, self.display_width, self.display_height, self.mm_to_px,
            self.tile_size, self.tile_line_width, self.line_width, self.wall_width, self.max_map_width,
            self.max_map_height, self.top_margin, self.left_margin, self.origin[0], self.origin[1]
        )
