from ozobotmapf.utils.constants import Directions, PositionTypes


class PathPosition:
    def __init__(self, time, max_time):
        if time < 0:
            self.time = 0
        elif time > max_time:
            self.time = max_time
        else:
            self.time = time

        self.pos_tile = None
        self.next_pos_tile = None
        self.enter_time, self.middle_time, self.leave_time = 0, 0, 0
        self.offset = 0
        self.is_first_half = False

    def set_position_tile(self, pos, next_pos):
        self.pos_tile = pos
        self.next_pos_tile = next_pos

    def set_time_window(self, enter, middle, leave):
        self.enter_time = enter
        self.middle_time = middle
        self.leave_time = leave

        if enter <= self.time < middle:
            self.offset = (self.time - enter) / (middle - enter)
            self.is_first_half = True
        else:
            self.offset = (self.time - middle) / (leave - middle)
            self.is_first_half = False

    def get_tile(self):
        return self.pos_tile.tile

    def is_turn(self):
        return self.pos_tile.is_turn

    def get_type(self):
        return self.pos_tile.type

    def get_point_from_position(self, bounded=False):
        middle = self.get_tile().get_middle()
        if self.is_first_half:
            point_from = self.get_tile().get_edge_middle(self.pos_tile.from_dir)
            point_to = middle
        else:
            point_from = middle
            point_to = self.get_tile().get_edge_middle(self.pos_tile.to_dir)

        position = point_from.offset_to(point_to, self.offset)
        return self.__bound_position_from_middle(position) if bounded else position

    def __bound_position_from_middle(self, position):
        if self.get_type() == PositionTypes.STOP:
            # Stop path before the tile middle
            enter = self.get_tile().get_edge_middle(self.pos_tile.from_dir)
            middle = self.get_tile().get_middle()
            bound = enter.offset_to(middle, 0.5)
            if bound.dist_to(middle) > position.dist_to(middle):
                return bound

        return position

    def get_angle_from_position(self, tile_size, line_width):
        origin, s_angle, e_angle = None, None, None

        if (self.is_first_half and self.get_type() == PositionTypes.START) or \
                (not self.is_first_half and self.get_type() == PositionTypes.STOP):
            return origin, s_angle, e_angle

        from_dir = self.pos_tile.previous_direction
        to_dir = self.pos_tile.next_direction
        origin = self.pos_tile.tile.get_middle().moved(-line_width / 2, -line_width / 2)

        if from_dir == Directions.UP:
            if to_dir == Directions.RIGHT:  # Left turn from Up (3)
                s_angle, e_angle = self.__left_turn_angles(from_dir)
                origin = origin.moved_direction(Directions.UP, tile_size)
            elif to_dir == Directions.LEFT:  # Right turn from Up (4)
                s_angle, e_angle = self.__right_turn_angles(from_dir)
                origin = origin.moved(-tile_size, -tile_size)
                return origin, s_angle, e_angle
        elif from_dir == Directions.DOWN:
            if to_dir == Directions.RIGHT:  # Right turn from Down (1)
                s_angle, e_angle = self.__right_turn_angles(from_dir)
                return origin, s_angle, e_angle
            elif to_dir == Directions.LEFT:  # Left turn from Down (2)
                s_angle, e_angle = self.__left_turn_angles(from_dir)
                origin = origin.moved_direction(Directions.LEFT, tile_size)
                return origin, s_angle, e_angle
        elif from_dir == Directions.RIGHT:
            if to_dir == Directions.UP:  # Right turn from Right (3)
                s_angle, e_angle = self.__right_turn_angles(from_dir)
                origin = origin.moved_direction(Directions.UP, tile_size)
                return origin, s_angle, e_angle
            elif to_dir == Directions.DOWN:  # Left turn from Right (1)
                s_angle, e_angle = self.__left_turn_angles(from_dir)
                return origin, s_angle, e_angle
        elif from_dir == Directions.LEFT:
            if to_dir == Directions.UP:  # Left turn from Left (4)
                s_angle, e_angle = self.__left_turn_angles(from_dir)
                origin = origin.moved(-tile_size, -tile_size)
            elif to_dir == Directions.DOWN:  # Right turn from Left (2)
                s_angle, e_angle = self.__right_turn_angles(from_dir)
                origin = origin.moved_direction(Directions.LEFT, tile_size)
        else:
            raise Exception("Getting arc path angle, but it is not a turn.")

        return origin, s_angle, e_angle

    def __left_turn_angles(self, from_dir):
        angle = 0
        if from_dir == Directions.DOWN:
            angle = 0 if self.is_first_half else 45
        elif from_dir == Directions.RIGHT:
            angle = 90 if self.is_first_half else 135
        elif from_dir == Directions.UP:
            angle = 180 if self.is_first_half else 225
        elif from_dir == Directions.LEFT:
            angle = 270 if self.is_first_half else 315
        angle1 = angle + (45 * self.offset)
        angle2 = angle1 - 3
        if angle1 < angle2:
            return angle1, angle2
        else:
            return angle2, angle1

    def __right_turn_angles(self, from_dir):
        angle = 0
        if from_dir == Directions.DOWN:
            angle = 180 if self.is_first_half else 135
        elif from_dir == Directions.RIGHT:
            angle = 270 if self.is_first_half else 225
        elif from_dir == Directions.UP:
            angle = 360 if self.is_first_half else 315
        elif from_dir == Directions.LEFT:
            angle = 90 if self.is_first_half else 45

        angle1 = angle - (45 * self.offset)
        angle2 = angle1 + 3
        if angle1 < angle2:
            return angle1, angle2
        else:
            return angle2, angle1

    def should_print_intersection(self):
        if self.next_pos_tile.is_turn and self.next_pos_tile.is_stop():
            return ((not self.is_turn()) and self.is_first_half and self.offset >= 0.45 and
                    self.pos_tile.intersection_cnt < 1 and self.get_type() == PositionTypes.PASS) or \
                   ((not self.is_turn()) and (not self.is_first_half) and self.offset >= 0.03 and
                    self.pos_tile.intersection_cnt < 2 and self.get_type() == PositionTypes.PASS) or \
                   ((not self.is_turn()) and (not self.is_first_half) and self.offset >= 0.6 and
                    self.pos_tile.intersection_cnt < 3 and self.get_type() == PositionTypes.PASS)
        else:
            return ((not self.is_turn()) and self.is_first_half and self.offset >= 0.45 and
                    self.pos_tile.intersection_cnt < 1 and self.get_type() == PositionTypes.PASS) or \
                   ((not self.is_turn()) and (not self.is_first_half) and self.offset >= 0.1 and
                    self.pos_tile.intersection_cnt < 2 and self.get_type() == PositionTypes.PASS) or \
                   ((not self.is_turn()) and (not self.is_first_half) and self.offset >= 0.75 and
                    self.pos_tile.intersection_cnt < 3 and self.get_type() == PositionTypes.PASS)

    def get_normal_directions(self):
        direction = self.pos_tile.from_dir if self.is_first_half else self.pos_tile.to_dir
        if direction in Directions.HORIZONTAL:
            return Directions.VERTICAL
        else:
            return Directions.HORIZONTAL
