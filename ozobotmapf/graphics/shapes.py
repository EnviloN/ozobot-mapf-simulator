from ozobotmapf.utils.constants import Directions


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

    def moved_direction(self, direction, by):
        if direction == Directions.UP:
            return self.moved(0, -by)
        elif direction == Directions.DOWN:
            return self.moved(0, by)
        elif direction == Directions.RIGHT:
            return self.moved(by, 0)
        elif direction == Directions.LEFT:
            return self.moved(-by, 0)
        else:
            return self

    def offset_to(self, other, offset):
        x_off = (other.x - self.x) * offset
        y_off = (other.y - self.y) * offset
        return self.moved(x_off, y_off)

    def to_list(self):
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


class Rectangle:
    def __init__(self, origin: Point, width: int, height: int):
        self.origin = Point(*origin.to_list())
        self.width = width
        self.height = height

    def to_list(self):
        return self.origin, self.width, self.height

    def __str__(self):
        return "Rectangle [Origin: {}, W: {}, H: {}]".format(self.origin, self.width, self.height)

    def __getitem__(self, item):
        if item == 0:
            return self.origin.x
        elif item == 1:
            return self.origin.y
        elif item == 2:
            return self.width
        elif item == 3:
            return self.height
        else:
            raise IndexError("Point has only two properties.")

    def __len__(self):
        return 4
