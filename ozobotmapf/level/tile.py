from ozobotmapf.graphics.shapes import Point
from ozobotmapf.level.ozomap_exception import OzoMapException
from ozobotmapf.utils.constants import Directions


class Tile:
    """Class represents a level tile.

    Attributes:
        origin (Point): Top-left point of the tile
        agent_start (int): ID of an agent that has starting point here (else 0)
        agent_finish (int): ID of an agent that has finish point here (else 0)
        __walls (list[bool]): Flags if there are walls around the tile (Format: [upper, right, bottom, left])
    """

    def __init__(self, origin=Point(0, 0), x_pos=0, y_pos=0, size=0):
        """Initialization of the Tile instance.

        Args:
            origin (Point): Top-left point of the tile
        """
        self.origin, self.x_pos, self.y_pos = origin, x_pos, y_pos
        self.agent_start = 0
        self.agent_finish = 0
        self.__walls = [False] * 4  # [upper, right, bottom, left]
        self.__size = size

    def is_start(self):
        """Returns true if there is an agent's start on the tile."""
        return True if self.agent_start > 0 else False

    def is_finish(self):
        """Returns true if there is an agent's finish on the tile."""
        return True if self.agent_finish > 0 else False

    def has_wall(self, direction):
        """Getter for upper wall."""
        return self.__walls[direction]

    def build_all_walls(self):
        """Sets all walls to True."""
        self.__walls = [True] * 4

    def build_wall(self, direction):
        """Sets upper wall to True."""
        self.__walls[direction] = True

    def destroy_all_walls(self):
        """Sets all walls to False."""
        self.__walls = [False] * 4

    def destroy_wall(self, direction):
        """Sets upper wall to False."""
        self.__walls[direction] = False

    def toggle_wall(self, direction):
        """Sets upper wall to the opposite value."""
        self.__walls[direction] = not self.__walls[direction]

    def direction_to(self, other):
        x, y = self.origin.to_list()
        x_other, y_other = other.origin.to_list()
        if x != x_other and y != y_other:
            raise OzoMapException("Diagonal directions are not supported.")
        elif x == x_other and y == y_other:
            return None
        elif x == x_other:
            return Directions.DOWN if y - y_other < 0 else Directions.UP
        elif y == y_other:
            return Directions.RIGHT if x - x_other < 0 else Directions.LEFT

    def get_middle(self):
        half_size = round(self.__size / 2)
        return self.origin.moved(half_size, half_size)

    def get_edge_middle(self, direction):
        half_size = round(self.__size / 2)
        if direction == Directions.UP:
            return self.origin.moved(half_size, 0)
        elif direction == Directions.RIGHT:
            return self.origin.moved(self.__size, half_size)
        elif direction == Directions.DOWN:
            return self.origin.moved(half_size, self.__size)
        elif direction == Directions.LEFT:
            return self.origin.moved(0, half_size)

