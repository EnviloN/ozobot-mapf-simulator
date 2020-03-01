import logging
import pygame

from ozobotmapf.utils.constants import Values, Colors


class Simulator:
    """Class handles object rendering on the screen and Window state.

    Attributes:
        __screen (pygame.Surface): Window screen where object are drawn
        __width (int): Window width
        __height (int): Window height
    """

    def __init__(self, config):
        """Initialization of Window.

        Pygame is initialized, real world dimensions from configuration are converted into pixels.
        All display and rendering parameters are computed.

        Args:
            config (Configuration): Application configuration parameters
        """
        logging.info("Initialising pygame and display.")
        pygame.init()
        if config.fullscreen:
            self.__screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        else:
            self.__screen = pygame.display.set_mode([config.window_width, config.window_height])
        pygame.display.set_caption(Values.APP_NAME)

        self.__screen.fill(Colors.WHITE)

        self.__width, self.__height = pygame.display.get_surface().get_size()
        logging.debug("Application window resolution: {} x {} (px)".format(self.__width, self.__height))
        self.config = config

    def update(self):
        """Updates pygame.display.

        Returns:
            Simulator: itself
        """
        pygame.display.update()
        return self

    def draw_map(self, ozomap):
        """Method draws given level to the screen.

        Firstly, all tiles are drawn, and then all walls are drawn.

        Args:
            ozomap (OzoMap): Map to be drawn

        Returns:
            Simulator: itself
        """
        self.__screen.fill(Colors.WHITE)

        for tile in ozomap.grid.tile_generator():
            self.__draw_tile(tile)

        self.__draw_walls(ozomap)
        return self

    def draw_full_path(self, positions):
        """Method draws the full path of a single agent.

        Args:
            positions (list[Tiles]): Agent's position list during plan execution

        Returns:
            Simulator: itself
        """
        half_size = self.config.tile_size / 2
        points = [pos.origin.moved(half_size, half_size) for pos in positions]

        self.__draw_following_path(points)
        return self

    def __draw_tile(self, tile):
        """Method draws a tile.

        If there is a start/end point for any agent, tile is filled with corresponding color. Then, borders
        are drawn around the tile.

        Args:
            tile (Tile): A tile to be drawn
        """
        tile_size = self.config.tile_size
        if tile.agent_start > 0 and tile.agent_finish > 0:
            self.__draw_double_color_tile(tile, 10)
        elif tile.agent_start > 0:
            self.__screen.fill(Colors.START, [tile.origin.x, tile.origin.y, tile_size, tile_size])
        elif tile.agent_finish > 0:
            self.__screen.fill(Colors.FINISH, [tile.origin.x, tile.origin.y, tile_size, tile_size])

        pygame.draw.rect(self.__screen, Colors.GREY, [tile.origin.x, tile.origin.y, tile_size, tile_size],
                         self.config.tile_border_width)

    def __draw_double_color_tile(self, tile, splits):
        colors = [Colors.START, Colors.FINISH]
        current_color = 0
        tile_size = self.config.tile_size
        part_size = tile_size / splits
        for part_x in range(splits):
            for part_y in range(splits):
                x = tile.origin.x + part_x * part_size
                y = tile.origin.y + part_y * part_size
                self.__screen.fill(colors[current_color], [x, y, part_size, part_size])
                current_color = 1 - current_color
            current_color = 1 - current_color

    def __draw_walls(self, ozomap):
        """Method all walls in the level.

        Args:
            ozomap (OzoMap): Map that is being drawn
        """
        for tile in ozomap.grid.tile_generator():
            if tile.has_upper_wall(): self.__draw_upper_wall(tile.origin)
            if tile.has_right_wall(): self.__draw_right_wall(tile.origin)
            if tile.has_bottom_wall(): self.__draw_bottom_wall(tile.origin)
            if tile.has_left_wall(): self.__draw_left_wall(tile.origin)

    def __draw_line_between_tiles(self, tile_from, tile_to):
        """Method draws following line between two tiles.

        Args:
            tile_from (Tile): Tile where the line should start
            tile_to (Tile): Tile where the line should end
        """
        half_size = self.config.tile_size / 2
        start = tile_from.origin.moved(half_size, half_size)
        end = tile_to.origin.moved(half_size, half_size)
        self.__draw_following_line(start, end)

    def __draw_upper_wall(self, tile_origin):
        """Method draws upper wall of a tile.

        Args:
            tile_origin (Point): Origin of a given tile
        """
        self.__draw_wall_line(tile_origin,
                              tile_origin.moved(self.config.tile_size, 0))

    def __draw_right_wall(self, tile_origin):
        """Method draws right wall of a tile.

        Args:
            tile_origin (Point): Origin of a given tile
        """
        self.__draw_wall_line(tile_origin.moved(self.config.tile_size, 0),
                              tile_origin.moved(self.config.tile_size, self.config.tile_size))

    def __draw_bottom_wall(self, tile_origin):
        """Method draws bottom wall of a tile.

        Args:
            tile_origin (Point): Origin of a given tile
        """
        self.__draw_wall_line(tile_origin.moved(self.config.tile_size, self.config.tile_size),
                              tile_origin.moved(0, self.config.tile_size))

    def __draw_left_wall(self, tile_origin):
        """Method draws left wall of a tile.

        Args:
            tile_origin (Point): Origin of a given tile
        """
        self.__draw_wall_line(tile_origin.moved(0, self.config.tile_size),
                              tile_origin)

    # def draw_tile_grid(self, ozomap):
    #     """Method draws level tile grid on the screen.
    #
    #     Tiles are not drawn individually. All horizontal lines are drawn, then all vertical lines.
    #
    #     Args:
    #         ozomap (OzoMap): Map of the problem
    #
    #     Returns:
    #         Window: itself
    #     """
    #     origin = ozomap.origin
    #
    #     # Horizontal lines
    #     line_length = len(ozomap.grid) * ozomap.tile_size
    #     for i in range(len(ozomap.grid[0]) + 1):
    #         offset = i * ozomap.tile_size
    #         start = Point(origin.x, origin.y + offset)
    #         end = Point(origin.x + line_length, origin.y + offset)
    #         self.__draw_tile_line(start, end)
    #
    #     # Vertical lines
    #     line_length = len(ozomap.grid[0]) * ozomap.tile_size
    #     for i in range(len(ozomap.grid) + 1):
    #         offset = i * ozomap.tile_size
    #         start = Point(origin.x + offset, origin.y)
    #         end = Point(origin.x + offset, origin.y + line_length)
    #         self.__draw_tile_line(start, end)
    #
    #     return self

    def __draw_tile_line(self, start, end):
        """Method draws a tile line from start to end.

        Note:
            Line width can be configured in the configuration file.

        Args:
            start (Point): Start point of the line
            end (Point): End point of the line
        """
        pygame.draw.line(self.__screen, Colors.GREY, start, end, self.config.tile_border_width)

    def __draw_wall_line(self, start, end):
        """Method draws a wall line from start to end.

        Note:
            Line width can be configured in the configuration file.

        Args:
            start (Point): Start point of the line
            end (Point): End point of the line
        """
        pygame.draw.line(self.__screen, Colors.BLACK, start, end, self.config.wall_width)

    def __draw_following_line(self, start, end):
        """Method draws a following line from start to end.

        Note:
            Line width can be configured in the configuration file.

        Args:
            start (Point): Start point of the line
            end (Point): End point of the line
        """
        pygame.draw.line(self.__screen, Colors.BLACK, start, end, self.config.line_width)

    def __draw_following_path(self, points):
        """Method draws following lines following the given list of points.

        Note:
            Line width can be configured in the configuration file.

        Args:
            points (list[Point]): List of points to draw a line between
        """
        pygame.draw.lines(self.__screen, Colors.BLACK, False, points, self.config.line_width)
