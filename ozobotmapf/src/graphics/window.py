import logging
import pygame
import time

from src.graphics.display_parameters import WindowParameters
from src.graphics.point import Point
from src.utils.constants import Colors, Values


class Window:
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
        self.parameters = WindowParameters(resolution, config)
        pygame.display.set_caption(Values.APP_NAME)

        self.screen.fill(Colors.WHITE)
        self.draw_tile_grid()
        pygame.display.update()

        self.width, self.height = pygame.display.get_surface().get_size()
        logging.debug("Application window resolution: {} x {} (px)".format(self.width, self.height))

    def draw_tile_grid(self):
        """Method draws all available tiles on the screen"""
        origin = self.parameters.origin

        # Horizontal lines
        line_length = self.parameters.max_map_width * self.parameters.tile_size
        for i in range(self.parameters.max_map_height + 1):
            offset = i*self.parameters.tile_size
            start = Point(origin.x, origin.y + offset)
            end = Point(origin.x + line_length, origin.y + offset)
            self.draw_tile_line(start, end)

        # Vertical lines
        line_length = self.parameters.max_map_height * self.parameters.tile_size
        for i in range(self.parameters.max_map_width + 1):
            offset = i * self.parameters.tile_size
            start = Point(origin.x + offset, origin.y)
            end = Point(origin.x + offset, origin.y + line_length)
            self.draw_tile_line(start, end)

    def draw_tile_line(self, start, end):
        """Method draws a tile line from start to end."""
        pygame.draw.line(self.screen, Colors.GREY, start, end, self.parameters.tile_line_width)
