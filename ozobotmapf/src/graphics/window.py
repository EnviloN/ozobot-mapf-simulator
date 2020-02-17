import logging
import pygame
import time

from src.graphics.window_parameters import WindowParameters
from src.graphics.point import Point
from src.map.map import Map
from src.utils.constants import Colors, Values


class Window:
    """Class handles object rendering on the screen and Window state.

    Attributes:
        __screen (pygame.Surface): Window screen where object are drawn
        parameters (WindowParameters): Parameters of the current application window
        __width (int): Window width
        __height (int): Window height
    """

    def __init__(self, resolution, fullscreen, config):
        """Initialization of Window.

        Pygame is initialized, real world dimensions from configuration are converted into pixels.
        All display and rendering parameters are computed.

        Args:
            resolution (list[int]): Width and height of the application window
            fullscreen (bool): Flag if window should run in fullscreen mode
            config (dict[str, dict[str, float]): Parsed configuration file
        """
        logging.info("Initialising pygame and display.")
        pygame.init()
        if fullscreen:
            self.__screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
            resolution = [config["display"]["resolution_width"], config["display"]["resolution_height"]]
        else:
            self.__screen = pygame.display.set_mode(resolution)
        self.parameters = WindowParameters(resolution, config)
        pygame.display.set_caption(Values.APP_NAME)

        self.__screen.fill(Colors.WHITE)

        self.__width, self.__height = pygame.display.get_surface().get_size()
        logging.debug("Application window resolution: {} x {} (px)".format(self.__width, self.__height))

    def update(self):
        """Updates pygame.display.

        Returns:
            Window: itself
        """
        pygame.display.update()
        return self

    def draw_tile_grid(self, mapp):
        """Method draws map tile grid on the screen.

        Tiles are not drawn individually. All horizontal lines are drawn, then all vertical lines.

        Args:
            mapp (Map): Map of the problem

        Returns:
            Window: itself
        """
        origin = mapp.origin

        # Horizontal lines
        line_length = len(mapp.grid) * mapp.tile_size
        for i in range(len(mapp.grid[0]) + 1):
            offset = i * mapp.tile_size
            start = Point(origin.x, origin.y + offset)
            end = Point(origin.x + line_length, origin.y + offset)
            self.__draw_tile_line(start, end)

        # Vertical lines
        line_length = len(mapp.grid[0]) * mapp.tile_size
        for i in range(len(mapp.grid) + 1):
            offset = i * mapp.tile_size
            start = Point(origin.x + offset, origin.y)
            end = Point(origin.x + offset, origin.y + line_length)
            self.__draw_tile_line(start, end)

        return self

    def __draw_tile_line(self, start, end):
        """Method draws a tile line from start to end.

        Note:
            Line width can be configured in the configuration file.

        Args:
            start (Point): Start point of the line
            end (Point): End point of the line
        """
        pygame.draw.line(self.__screen, Colors.GREY, start, end, self.parameters.tile_line_width)