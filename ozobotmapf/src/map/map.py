from src.graphics.point import Point
from src.map.tile import Tile


class Map:
    """Class represents the map of the problem.

    Attributes:
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
        self.origin = window_params.origin
        self.tile_size = window_params.tile_size
        self.grid = [[Tile(Point(0, 0))] * window_params.max_map_height] * window_params.max_map_width
        for x in range(len(self.grid)):
            for y in range(len(self.grid[0])):
                self.grid[x][y] = Tile(self.origin.moved_copy(x*self.tile_size, y*self.tile_size))
