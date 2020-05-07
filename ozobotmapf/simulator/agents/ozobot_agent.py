from ozobotmapf.graphics.drawables import Circle
from ozobotmapf.simulator.agents.agent import Agent
from ozobotmapf.simulator.agents.path_drawable import UTurnCode, PathSegment, TurnSegment
from ozobotmapf.utils.constants import PositionTypes


class OzobotAgent(Agent):
    """
    This agent is animating it's path in time, keeps Ozobot's limitations in mind, and uses Color Codes.
    Agent also supports curved paths.
    """
    def __init__(self, agent_id, raw_plans, ozomap, config):
        super().__init__(agent_id, raw_plans, ozomap, config)
        self.tail = []

    def update_path(self, time):
        self.active_path.clear()
        self.__filter_tail(time)
        self.__update_tail(time)

        position = self._get_position(time)
        self.__add_path_segments(position)

        if position.pos_tile.u_turn and not position.is_first_half:
            self.__add_color_code(position, time)

        self.__activate_tail()

    def __add_path_segments(self, pos):
        if pos.get_type() == PositionTypes.WAIT:
            return

        if pos.is_turn() and pos.get_type() != PositionTypes.STOP:
            self.__add_arc_segment(pos)
        else:
            if self.config.colors and pos.should_print_intersection():
                self.__add_intersection_segments(pos)
            else:  # No intersection, just path
                if not (pos.get_type() == PositionTypes.STOP and pos.is_turn()):
                    self.__add_path_line_segments(pos)
                else:
                    self.__add_turn_wait_segment()

    def __add_arc_segment(self, pos):
        box_origin, s_angle, e_angle = pos.get_angle_from_position(self.config.tile_size, self.config.line_width)
        if box_origin:
            self.tail.append(TurnSegment(
                self._arc_drawable(box_origin, s_angle, e_angle),
                pos.time, self.config.tail_lag, self.config.colors)
            )

    def __add_color_code(self, pos, time):
        pos.pos_tile.u_turn = False
        circle = Circle(pos.pos_tile.tile.get_middle(), self.config.color_code_radius)
        code = UTurnCode(circle, time, self.config.tail_lag)
        self.tail.append(code)

    def __add_intersection_segments(self, pos):
        point = pos.get_point_from_position(True)
        p1, p2 = self.__get_intersection_indicator_ends(point, pos)
        if pos.next_pos_tile.is_turn and not pos.is_first_half:  # Intersection right before a turn
            self.tail.append(
                TurnSegment(self._line_drawable(p1, p2), pos.time,
                            self.config.tail_lag, self.config.colors)
            )
            self.tail.append(
                TurnSegment(self._line_drawable(point, point.moved_direction(pos.pos_tile.from_dir, 15)), pos.time,
                            self.config.tail_lag, self.config.colors)
            )
        else:  # Any other intersection
            self.tail.append(
                PathSegment(self._line_drawable(p1, p2), pos.time, self.config.tail_lag, self.config.colors)
            )
            self.tail.append(
                PathSegment(self._line_drawable(point, point.moved_direction(pos.pos_tile.from_dir, 15)), pos.time,
                            self.config.tail_lag, self.config.colors)
            )
        pos.pos_tile.intersection_cnt += 1

    def __get_intersection_indicator_ends(self, point, pos):
        dir1, dir2 = pos.get_normal_directions()
        p1 = point.moved_direction(dir1, self.config.intersection_width / 2)
        p2 = point.moved_direction(dir2, self.config.intersection_width / 2)
        return p1, p2

    def __add_path_line_segments(self, pos):
        point = pos.get_point_from_position(True)
        if pos.next_pos_tile.is_turn and not pos.is_first_half and pos.offset >= 0.65:
            # Path before a turn (but after the intersection)
            self.tail.append(
                TurnSegment(self._line_drawable(point, point), pos.time, self.config.tail_lag, self.config.colors)
            )
        else:
            self.tail.append(
                PathSegment(self._line_drawable(point, point), pos.time, self.config.tail_lag, self.config.colors)
            )

    def __add_turn_wait_segment(self, pos):
        entry = pos.get_tile().get_edge_middle(pos.pos_tile.previous_direction)
        p = pos.get_tile().get_middle().moved_direction(pos.pos_tile.next_direction, self.config.tile_size / 3)
        self.tail.append(
            PathSegment(self._line_drawable(entry, entry.offset_to(p, 0.5)), pos.time,
                        self.config.tail_lag, self.config.colors)
        )

    def __filter_tail(self, time):
        while len(self.tail) > 0 and not self.tail[0].is_valid(time):
            self.tail = self.tail[1:]

    def __update_tail(self, time):
        for p_drawable in self.tail:
            p_drawable.update(time)

    def __activate_tail(self):
        for p_drawable in self.tail:
            self.active_path.add_drawable(p_drawable.drawable)
