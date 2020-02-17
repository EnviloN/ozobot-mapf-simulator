
class Point:
    """Class representing point in 2D space."""
    def __init__(self, x: int, y: int):
        self.x, self.y = x, y

    def __getitem__(self, item):
        if item == 0:
            return self.x
        elif item == 1:
            return self.y
        else:
            raise IndexError("Point has only two properties.")

    def __len__(self):
        return 2
