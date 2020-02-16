import logging
import math


class DisplayParameters:
    """Class computes and stores all display and rendering parameters."""

    def __init__(self, resolution, display_config, ozobot_config):
        """Creates an instance of DisplayParameters and initializes itself."""
        self.window_width = resolution[0]
        self.window_height = resolution[1]
        self.display_width = display_config["resolution_width"]
        self.display_height = display_config["resolution_height"]

        self.mm_to_px = \
            ((display_config["resolution_width"] / display_config["display_width"]) +
             (display_config["resolution_height"] / display_config["display_height"])) / 2

        self.tile_size = round(ozobot_config["tile_size"] * self.mm_to_px)
        self.tile_line_width = math.floor(ozobot_config["tile_line_width"] * self.mm_to_px)
        self.line_width = round(ozobot_config["line_width"] * self.mm_to_px)
        self.wall_width = round(ozobot_config["wall_width"] * self.mm_to_px)

        self.max_map_width = math.floor(self.window_width / self.tile_size)
        self.max_map_height = math.floor(self.window_height / self.tile_size)

        self.top_margin = math.floor((self.window_height - (self.tile_size * self.max_map_height)) / 2)
        self.left_margin = math.floor((self.window_width - (self.tile_size * self.max_map_width)) / 2)

        self.origin = [self.left_margin, self.top_margin]

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
