class Point:
    """Class representing a point in 2D space.

    Point(0, 0) is located in the top-left corner of the application window.

    Attributes:
        x (int): X coordinate (vertical axis)
        y (int): Y coordinate (horizontal axis)
    """

    def __init__(self, x: int, y: int):
        """Initialization of Point instance.

        Args:
            x (int): X coordinate (vertical axis)
            y (int): Y coordinate (horizontal axis)
        """
        self.x, self.y = x, y

    def moved(self, x, y):
        """Method creates a copy of the point moved by x and y.

        Args:
            x (int): Length by which the point should be moved along the X axis
            y (int): Length by which the point should be moved along the Y axis

        Returns:
            Point: New point instance moved by x and y
        """
        return Point(self.x + x, self.y + y)

    def to_pair(self):
        """Method returns the point in a pair representation."""
        return self.x, self.y

    def __str__(self):
        return "Point [{}, {}]".format(self.x, self.y)

    def __getitem__(self, item):
        if item == 0:
            return self.x
        elif item == 1:
            return self.y
        else:
            raise IndexError("Point has only two properties.")

    def __len__(self):
        return 2
