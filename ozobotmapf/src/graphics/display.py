import logging
import pygame
import time

from src.graphics.display_parameters import DisplayParameters
from src.utils.constants import Colors, Values


class Display:
    """Class handles object rendering on the screen."""

    def __init__(self, resolution, fullscreen, config):
        """Creates Display instance and initializes itself.

        Pygame is initialized, real world dimensions from configuration are converted into pixels.
        All display and rendering parameters are computed.
        """
        logging.info("Initialising pygame and display.")
        pygame.init()
        if fullscreen:
            self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
            resolution = [config["display"]["resolution_width"], config["display"]["resolution_height"]]
        else:
            self.screen = pygame.display.set_mode(resolution)
        self.parameters = DisplayParameters(resolution, config)
        pygame.display.set_caption(Values.APP_NAME)

        self.screen.fill(Colors.WHITE)
        self.draw_tiles()
        pygame.display.update()

        self.width, self.height = pygame.display.get_surface().get_size()
        logging.debug("Application resolution: {} x {} (px)".format(self.width, self.height))

    def draw_tiles(self):
        """Method draws all available tiles on the screen"""
        # TODO: Create Point class and start using it instead of [x,y]
        origin = [self.parameters.left_margin, self.parameters.top_margin]

        # Horizontal lines
        line_length = self.parameters.max_map_width * self.parameters.tile_size
        for i in range(self.parameters.max_map_height + 1):
            offset = i*self.parameters.tile_size
            start = [origin[0], origin[1] + offset]
            end = [origin[0] + line_length, origin[1] + offset]
            self.draw_tile_line(start, end)

        # Vertical lines
        line_length = self.parameters.max_map_height * self.parameters.tile_size
        for i in range(self.parameters.max_map_width + 1):
            offset = i * self.parameters.tile_size
            start = [origin[0] + offset, origin[1]]
            end = [origin[0] + offset, origin[1] + line_length]
            self.draw_tile_line(start, end)

    def draw_tile_line(self, start, end):
        """Method draws a tile line from start to end."""
        pygame.draw.line(self.screen, Colors.BLACK, start, end, self.parameters.tile_line_width)
