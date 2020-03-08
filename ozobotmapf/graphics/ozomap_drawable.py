from ozobotmapf.graphics.drawables import DrawableGroup, FillChecker, FillRect, Line
from ozobotmapf.graphics.shapes import Rectangle, Point
from ozobotmapf.utils.constants import Colors, Directions


class OzomapDrawableParser:
    def __init__(self, ozomap, config):
        self.ozomap = ozomap
        self.config = config

    def parse(self):
        drawables = [self.__positions_to_drawable(), self.__borders_to_drawable(), self.__walls_to_drawable()]
        return drawables

    def __positions_to_drawable(self):
        group = DrawableGroup()
        for tile in self.ozomap.map_tile_generator():
            rectangle = Rectangle(Point(tile.origin.x, tile.origin.y), self.config.tile_size, self.config.tile_size)
            if tile.agent_start > 0 and tile.agent_finish > 0:
                group.add_drawable(FillChecker(rectangle, Colors.START, Colors.FINISH))
            elif tile.agent_start > 0:
                group.add_drawable(FillRect(rectangle, Colors.START))
            elif tile.agent_finish > 0:
                group.add_drawable(FillRect(rectangle, Colors.FINISH))
        return group

    def __borders_to_drawable(self):
        group = DrawableGroup()
        origin = self.ozomap.get_origin()

        # Horizontal lines
        line_length = self.ozomap.grid.width * self.config.tile_size
        for i in range(self.ozomap.grid.height + 1):
            offset = i * self.config.tile_size
            start = Point(origin.x, origin.y + offset)
            end = Point(origin.x + line_length, origin.y + offset)
            group.add_drawable(Line(start, end, self.config.tile_border_width, Colors.GREY))

        # Vertical lines
        line_length = self.ozomap.grid.height * self.config.tile_size
        for i in range(self.ozomap.grid.width + 1):
            offset = i * self.config.tile_size
            start = Point(origin.x + offset, origin.y)
            end = Point(origin.x + offset, origin.y + line_length)
            group.add_drawable(Line(start, end, self.config.tile_border_width, Colors.GREY))
        return group

    def __walls_to_drawable(self):
        wall_set = set()
        for tile in self.ozomap.map_tile_generator():
            if tile.has_wall(Directions.UP):
                wall_set.add(self.__upper_wall_to_drawable(tile.origin))
            if tile.has_wall(Directions.RIGHT):
                wall_set.add(self.__right_wall_to_drawable(tile.origin))
            if tile.has_wall(Directions.DOWN):
                wall_set.add(self.__bottom_wall_to_drawable(tile.origin))
            if tile.has_wall(Directions.LEFT):
                wall_set.add(self.__left_wall_to_drawable(tile.origin))
        group = DrawableGroup()
        for wall in wall_set:
            group.add_drawable(wall)
        return group

    def __upper_wall_to_drawable(self, tile_origin):
        return self.__wall_line_to_drawable(tile_origin,
                              tile_origin.moved(self.config.tile_size, 0))

    def __right_wall_to_drawable(self, tile_origin):
        return self.__wall_line_to_drawable(tile_origin.moved(self.config.tile_size, 0),
                              tile_origin.moved(self.config.tile_size, self.config.tile_size))

    def __bottom_wall_to_drawable(self, tile_origin):
        return self.__wall_line_to_drawable(tile_origin.moved(self.config.tile_size, self.config.tile_size),
                              tile_origin.moved(0, self.config.tile_size))

    def __left_wall_to_drawable(self, tile_origin):
        return self.__wall_line_to_drawable(tile_origin.moved(0, self.config.tile_size),
                              tile_origin)

    def __wall_line_to_drawable(self, start, end):
        return Line(start, end, self.config.wall_width)