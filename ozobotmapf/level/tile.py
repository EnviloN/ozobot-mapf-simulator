from ozobotmapf.graphics.shapes import Point


class Tile:
    """Class represents a level tile.

    Attributes:
        origin (Point): Top-left point of the tile
        agent_start (int): ID of an agent that has starting point here (else 0)
        agent_finish (int): ID of an agent that has finish point here (else 0)
        __walls (list[bool]): Flags if there are walls around the tile (Format: [upper, right, bottom, left])
    """

    def __init__(self, origin=Point(0, 0), x_pos=0, y_pos=0):
        """Initialization of the Tile instance.

        Args:
            origin (Point): Top-left point of the tile
        """
        self.origin, self.x_pos, self.y_pos = origin, x_pos, y_pos
        self.agent_start = 0
        self.agent_finish = 0
        self.__walls = [False] * 4  # [upper, right, bottom, left]

    def is_start(self):
        """Returns true if there is an agent's start on the tile."""
        return True if self.agent_start > 0 else False

    def is_finish(self):
        """Returns true if there is an agent's finish on the tile."""
        return True if self.agent_finish > 0 else False

    def has_upper_wall(self):
        """Getter for upper wall."""
        return self.__walls[0] is True

    def has_right_wall(self):
        """Getter for right wall."""
        return self.__walls[1] is True

    def has_bottom_wall(self):
        """Getter for bottom wall."""
        return self.__walls[2] is True

    def has_left_wall(self):
        """Getter for left wall."""
        return self.__walls[3] is True

    def build_all_walls(self):
        """Sets all walls to True."""
        self.__walls = [True] * 4

    def build_upper_wall(self):
        """Sets upper wall to True."""
        self.__walls[0] = True

    def build_right_wall(self):
        """Sets right wall to True."""
        self.__walls[1] = True

    def build_bottom_wall(self):
        """Sets bottom wall to True."""
        self.__walls[2] = True

    def build_left_wall(self):
        """Sets left wall to True."""
        self.__walls[3] = True

    def destroy_all_walls(self):
        """Sets all walls to False."""
        self.__walls = [False] * 4

    def destroy_upper_wall(self):
        """Sets upper wall to False."""
        self.__walls[0] = False

    def destroy_right_wall(self):
        """Sets right wall to False."""
        self.__walls[1] = False

    def destroy_bottom_wall(self):
        """Sets bottom wall to False."""
        self.__walls[2] = False

    def destroy_left_wall(self):
        """Sets left wall to False."""
        self.__walls[3] = False

    def toggle_upper_wall(self):
        """Sets upper wall to the opposite value."""
        self.__walls[0] = not self.__walls[0]

    def toggle_right_wall(self):
        """Sets right wall to the opposite value."""
        self.__walls[1] = not self.__walls[1]

    def toggle_bottom_wall(self):
        """Sets bottom wall to the opposite value."""
        self.__walls[2] = not self.__walls[2]

    def toggle_left_wall(self):
        """Sets left wall to the opposite value."""
        self.__walls[3] = not self.__walls[3]