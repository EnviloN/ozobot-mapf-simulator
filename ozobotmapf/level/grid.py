from ozobotmapf.level.tile import Tile


class Grid:
    def __init__(self, config):
        self.__origin = config.map_origin
        self.__tile_size = config.tile_size
        self.__tiles = [[Tile() for _ in range(config.max_map_width)] for _ in
                        range(config.max_map_height)]
        self.width, self.height = config.max_map_width, config.max_map_height

        for col in range(len(self.__tiles[0])):
            for row in range(len(self.__tiles)):
                tile_origin = self.__origin.moved(col * self.__tile_size, row * self.__tile_size)
                self.__tiles[row][col] = Tile(tile_origin, col, row)

    def get_tile(self, x, y):
        return self.__tiles[y][x]

    def tile_generator(self):
        for col in range(len(self.__tiles[0])):
            for row in range(len(self.__tiles)):
                yield self.__tiles[row][col]

    def get_origin(self):
        return self.__origin
