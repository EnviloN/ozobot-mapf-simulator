class Tile:
    """Class represents a map tile.

    Attributes:
        __origin (Point): Top-left point of the tile
    """

    def __init__(self, origin):
        """Initialization of the Tile instance.

        Args:
            origin (Point): Top-left point of the tile
        """
        self.__origin = origin
