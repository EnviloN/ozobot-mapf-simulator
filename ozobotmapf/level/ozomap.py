import logging
import re
import itertools

from ozobotmapf.graphics.shapes import Point
from ozobotmapf.level.grid import Grid
from ozobotmapf.level.ozomap_exception import OzoMapException
from ozobotmapf.level.tile import Tile
from ozobotmapf.utils.constants import Directions


class OzoMap:
    """Class represents the level of the problem.

    Attributes:
        width (int): True width of the level
        height (int): True height of the level
        agent_cnt (int): Number of agents on the level
        grid (Grid): 2D grid of tiles
    """

    def __init__(self, config):
        """Initialization of Map instance.

        The 2D grid of tiles is created.

        Args:
            config (Configuration): Application configuration parameters
        """
        self.width, self.height, self.agent_cnt = 0, 0, 0
        self.grid = Grid(config)

    def init_empty_map(self, config):
        """Initialize an empty level only with border walls.

        Args:
            config (Configuration): Application configuration parameters"""
        self.width, self.height, self.agent_cnt = config.map_width, config.map_height, config.map_agent_count
        self.__validate_attributes()

        for tile in self.map_tile_generator():
            if tile.y_pos == 0:
                tile.build_wall(Directions.UP)
            if tile.y_pos == (self.height - 1):
                tile.build_wall(Directions.DOWN)
            if tile.x_pos == 0:
                tile.build_wall(Directions.LEFT)
            if tile.x_pos == (self.width - 1):
                tile.build_wall(Directions.RIGHT)

        logging.info("Empty Map successfully initialized.")

    def load_map(self, config):
        """Method loads level from a file.

        First, the level height and width are set, as well as number of agents. These parameters are validated and then
        the level is built.

        Args:
            config (Configuration): Application configuration

        Returns:
            OzoMap: itself
        """
        logging.info("Loading level.")
        with open(config.map_path, "r") as file:
            lines = file.readlines()

        self.width, self.height, self.agent_cnt = config.map_width, config.map_height, config.map_agent_count
        self.__validate_attributes()
        self.__build_map(lines)

        logging.info("Map successfully loaded.")
        logging.debug("Map: {}x{} tiles, {} agents.".format(self.width, self.height, self.agent_cnt))

        return self

    def get_origin(self):
        """Getter for the map (grid) origin.

        Returns:
            Point: Origin of the map grid
        """
        return self.grid.get_origin()

    def map_tile_generator(self):
        """Map tile generator that yields all map tiles."""
        for x in range(self.width):
            for y in range(self.height):
                yield self.grid.get_tile(x, y)

    def get_tiles_from_agent_positions(self, positions, waiting=True):
        """Method returns list of tiles for given agent's position list.

        Args:
            positions (list[int]): Agent's positions (tile IDs) during the plan execution
            waiting (bool): If false, consecutive duplicates from positions are removed

        Returns:
            list[Tiles]: List of tile instances for given agent's positions
        """
        if waiting:
            return [self.get_tile_by_id(tile_id) for tile_id in positions]
        else:
            return [self.get_tile_by_id(tile_id) for tile_id in [group[0] for group in itertools.groupby(positions)]]

    def __validate_attributes(self):
        """Method validates level width, height and agent count."""
        if self.width > self.grid.width or self.height > self.grid.height:
            raise_exception("Map is too big for the target display.")
        if self.agent_cnt > self.width * self.height:
            raise_exception("Too many agents in the level.")

    def __build_map(self, lines):
        """Method builds the level from graph representation.

        Map tiles are initialized, then all the excessive walls are destroyed.

        Args:
            lines (list[str]): Lines from the level file containing the graph representation of the level.
        """
        if lines[0] != "V =\n" or lines[self.width * self.height + 1] != "E =\n":
            raise_exception("OzoMap file has invalid syntax.")

        tiles = lines[1:self.width * self.height + 1]
        edges = lines[self.width * self.height + 2:]

        self.__init_tiles(tiles)
        self.__destroy_walls(edges)

    def __init_tiles(self, tiles):
        """Method initializes all level tiles.

        All four walls are built (set to True) around the tile and if there is a start/end point for any agent
        on the tile, these values are updated.

        Args:
            tiles (list[str]): Lines from level file that contain tiles (graph vertices)
        """
        for tile in tiles:
            tile_id, start, end = map(int, re.compile("\((\d+),(\d+),(\d+)\)").match(tile).groups())
            x, y = self.__get_position_from_id(tile_id)
            self.grid.get_tile(x, y).agent_start = start
            self.grid.get_tile(x, y).agent_finish = end
            self.grid.get_tile(x, y).build_all_walls()

    def __destroy_walls(self, edges):
        """Method destroys excessive walls around tiles.

        If there is an edge (in graph representation) between tiles, the corresponding wall is destroyed in both
        tiles.

        Args:
            edges (list[str]): Lines from level file that contain graph edges
        """
        for edge in edges:
            from_id, to_id = map(int, re.compile("{(\d+),(\d+)}").match(edge).groups())
            x_from, y_from = self.__get_position_from_id(from_id)
            x_to, y_to = self.__get_position_from_id(to_id)

            if x_from == x_to:
                if y_from < y_to:
                    self.grid.get_tile(x_from, y_from).destroy_wall(Directions.DOWN)
                    self.grid.get_tile(x_to, y_to).destroy_wall(Directions.UP)
                else:
                    self.grid.get_tile(x_from, y_from).destroy_wall(Directions.UP)
                    self.grid.get_tile(x_to, y_to).destroy_wall(Directions.DOWN)
            elif y_from == y_to:
                if x_from < x_to:
                    self.grid.get_tile(x_from, y_from).destroy_wall(Directions.RIGHT)
                    self.grid.get_tile(x_to, y_to).destroy_wall(Directions.LEFT)
                else:
                    self.grid.get_tile(x_from, y_from).destroy_wall(Directions.LEFT)
                    self.grid.get_tile(x_to, y_to).destroy_wall(Directions.RIGHT)

    def get_tile_by_id(self, tile_id):
        """Method returns a tile instance with given tile_id

        Args:
            tile_id (int): Number of the tile

        Returns:
            Tile: Instance of tile with given tile_id
        """
        x, y = self.__get_position_from_id(tile_id)
        return self.grid.get_tile(x, y)

    def __get_position_from_id(self, tile_id):
        """Method computes which tile (row and column) corresponds to tile ID.

        Args:
            tile_id (int): Number of the tile

        Returns:
            (int, int): Tuple of row and column of the tile grid
        """
        return tile_id % self.width, tile_id // self.width
# ------------------------------------------------------------------------------------------------------------


def raise_exception(message):
    """Method logs the error and raises exception.

    Raises:
        OzoMapException
    """
    logging.error(message)
    raise OzoMapException(message)
