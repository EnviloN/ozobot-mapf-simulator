class Tile:
    """Class represents a level tile.

    Attributes:
        origin (Point): Top-left point of the tile
        start_agent (int): ID of an agent that has starting point here (else 0)
        finish_agent (int): ID of an agent that has finish point here (else 0)
        walls (list[bool]): Flags if there are walls around the tile (Format: [upper, right, bottom, left])
    """

    def __init__(self, origin):
        """Initialization of the Tile instance.

        Args:
            origin (Point): Top-left point of the tile
        """
        self.origin = origin
        self.start_agent = 0
        self.finish_agent = 0
        self.walls = [False] * 4  # [upper, right, bottom, left]

    def destroy_upper_wall(self):
        """Sets upper wall to False."""
        self.walls[0] = False

    def destroy_right_wall(self):
        """Sets right wall to False."""
        self.walls[1] = False

    def destroy_bottom_wall(self):
        """Sets bottom wall to False."""
        self.walls[2] = False

    def destroy_left_wall(self):
        """Sets left wall to False."""
        self.walls[3] = False

    def has_upper_wall(self):
        """Getter for upper wall."""
        return self.walls[0] is True

    def has_right_wall(self):
        """Getter for right wall."""
        return self.walls[1] is True

    def has_bottom_wall(self):
        """Getter for bottom wall."""
        return self.walls[2] is True

    def has_left_wall(self):
        """Getter for left wall."""
        return self.walls[3] is True
