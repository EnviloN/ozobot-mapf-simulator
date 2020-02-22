import logging
import re

from src.graphics.point import Point
from src.map.ozomap_exception import OzoMapException
from src.map.tile import Tile


class OzoMap:
    """Class represents the map of the problem.

    Attributes:
        width (int): True width of the map
        height (int): True height of the map
        agent_cnt (int): Number of agents on the map
        origin (Point): Top-left point of the map
        tile_size (int): Length of the tile side
        grid (list[list[Tile]]): 2D grid of tiles
    """

    def __init__(self, window_params):
        """Initialization of Map instance.

        The 2D grid of tiles is created.

        Args:
            window_params (WindowParameters): Parameters of the application window
        """
        self.width, self.height, self.agent_cnt = 0, 0, 0
        self.origin = window_params.origin
        self.tile_size = window_params.tile_size
        window_params.tile_size += 1  # This needs to be done for tile borders to overlap during drawing
        self.grid = [[Tile(Point(0, 0)) for _ in range(window_params.max_map_height)] for _ in
                     range(window_params.max_map_width)]
        for x in range(len(self.grid)):
            for y in range(len(self.grid[0])):
                self.grid[x][y] = Tile(self.origin.moved_copy(x * self.tile_size, y * self.tile_size))

    def load_map(self, path):
        """Method loads map from a file.

        First, the map height and width are set, as well as number of agents. These parameters are validated and then
        the map is built.

        Args:
            path (string): Path to the map file
        """
        logging.info("Loading map.")
        with open(path, "r") as file:
            lines = file.readlines()

        try:
            self.width, self.height = [int(x) for x in lines[0].split("x")]
            self.agent_cnt = int(lines[1])
        except ValueError:
            raise OzoMapException("OzoMap file has invalid syntax.")

        if self.width > len(self.grid) or self.height > len(self.grid[0]):
            raise OzoMapException("Map is too big for the target display.")
        if self.agent_cnt >= self.width * self.height:
            raise OzoMapException("Too many agents in the map.")

        lines = lines[2:]
        # TODO: Save lines in a temp file for MAPF solver to use

        self.__build_map(lines)

        logging.info("Map successfully loaded.")
        logging.debug("Map: {}x{} tiles, {} agents.".format(self.width, self.height, self.agent_cnt))

    def __build_map(self, lines):
        """Method builds the map from graph representation.

        Map tiles are initialized, then all the excessive walls are destroyed.

        Args:
            lines (list[str]): Lines from the map file containing the graph representation of the map.
        """
        if lines[0] != "V =\n" or lines[self.width * self.height + 1] != "E =\n":
            raise OzoMapException("OzoMap file has invalid syntax.")

        tiles = lines[1:self.width * self.height + 1]
        edges = lines[self.width * self.height + 2:]

        self.__init_tiles(tiles)
        self.__destroy_walls(edges)

    def __init_tiles(self, tiles):
        """Method initializes all map tiles.

        All four walls are built (set to True) around the tile and if there is a start/end point for any agent
        on the tile, these values are updated.

        Args:
            tiles (list[str]): Lines from map file that contain tiles (graph vertices)
        """
        for tile in tiles:
            tile_id, start, end = map(int, re.compile("\((\d+),(\d+),(\d+)\)").match(tile).groups())
            x, y = self.__get_position_from_id(tile_id)
            self.grid[x][y].start_agent = start
            self.grid[x][y].finish_agent = end
            self.grid[x][y].walls = [True] * 4

    def __destroy_walls(self, edges):
        """Method destroys excessive walls around tiles.

        If there is an edge (in graph representation) between tiles, the corresponding wall is destroyed in both
        tiles.

        Args:
            edges (list[str]): Lines from map file that contain graph edges
        """
        for edge in edges:
            from_id, to_id = map(int, re.compile("{(\d+),(\d+)}").match(edge).groups())
            x_from, y_from = self.__get_position_from_id(from_id)
            x_to, y_to = self.__get_position_from_id(to_id)

            if x_from == x_to:
                if y_from < y_to:
                    self.grid[x_from][y_from].destroy_bottom_wall()
                    self.grid[x_to][y_to].destroy_upper_wall()
                else:
                    self.grid[x_from][y_from].destroy_upper_wall()
                    self.grid[x_to][y_to].destroy_bottom_wall()
            elif y_from == y_to:
                if x_from < x_to:
                    self.grid[x_from][y_from].destroy_right_wall()
                    self.grid[x_to][y_to].destroy_left_wall()
                else:
                    self.grid[x_from][y_from].destroy_left_wall()
                    self.grid[x_to][y_to].destroy_right_wall()

    def __get_position_from_id(self, tile_id):
        """Method computes which tile (row and column) corresponds to tile ID.

        Args:
            tile_id (int): Number of the tile

        Returns:
            (int, int): Tuple of row and column of the tile grid
        """
        return tile_id % self.width, tile_id // self.width
