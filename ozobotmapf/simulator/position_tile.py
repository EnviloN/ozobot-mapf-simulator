from ozobotmapf.utils.constants import PositionTypes, Directions


class PositionTile:
    def __init__(self, tile, from_dir, to_dir):
        self.tile = tile
        self.from_dir = from_dir
        self.to_dir = to_dir

        self.previous_direction = Directions.NONE
        self.next_direction = Directions.NONE

        self.type = self.__get_type()
        self.is_turn = False
        self.u_turn = False
        self.intersection_cnt = 0

    def __get_type(self):
        if self.from_dir == Directions.NONE and self.to_dir == Directions.NONE:
            return PositionTypes.WAIT
        elif self.from_dir == Directions.NONE:
            return PositionTypes.START
        elif self.to_dir == Directions.NONE:
            return PositionTypes.STOP
        else:
            return PositionTypes.PASS

    def set_movement_directions(self, from_dir, to_dir):
        self.previous_direction = from_dir
        self.next_direction = to_dir

        vertical = {Directions.UP, Directions.DOWN}
        horizontal = {Directions.RIGHT, Directions.LEFT}
        if self.previous_direction in horizontal and self.next_direction in vertical:
            self.is_turn = True
        elif self.previous_direction in vertical and self.next_direction in horizontal:
            self.is_turn = True

        if self.type == PositionTypes.STOP and self.previous_direction == self.next_direction:
            self.u_turn = True