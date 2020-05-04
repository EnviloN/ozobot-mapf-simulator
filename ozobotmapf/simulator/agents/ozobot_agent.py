import math

from ozobotmapf.graphics.drawables import Circle
from ozobotmapf.simulator.agents.agent import Agent
from ozobotmapf.simulator.agents.path_drawable import PathDrawable, UTurnCode, PathSegment
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
        self.__add_drawables(position)

        if position.pos_tile.u_turn and not position.is_first_half:
            self.__add_color_code(position, time)

        self.__activate_tail()

    def __add_drawables(self, pos):
        if pos.pos_tile.type != PositionTypes.WAIT:
            if pos.pos_tile.is_turn and not (pos.pos_tile.type == PositionTypes.START):
                box_origin, s_angle, e_angle = pos.get_angle_from_position(self.config.tile_size, self.config.line_width)
                if box_origin:
                    if self.config.colors and pos.should_print_intersection():
                        center_move = self.config.tile_size / 2 + self.config.line_width / 2
                        radius = self.config.tile_size / 2
                        center = box_origin.moved(center_move, center_move)
                        x = radius * math.cos(math.radians(s_angle))
                        y = radius * math.sin(math.radians(s_angle))
                        point = center.moved(x, -y)
                        p1 = center.offset_to(point, 0.7)
                        p2 = center.offset_to(point, 1.3)
                        self.tail.append(PathSegment(
                            self._line_drawable(p1, p2),
                            pos.time, self.config.tail_lag, self.config.colors))
                        pos.pos_tile.intersection_cnt += 1
                    else:
                        self.tail.append(PathSegment(
                            self._arc_drawable(box_origin, s_angle, e_angle),
                            pos.time, self.config.tail_lag, self.config.colors)
                        )
            else:
                point = pos.get_point_from_position()
                if self.config.colors and pos.should_print_intersection():
                    dir1, dir2 = pos.get_normal_directions()
                    p1 = point.moved_direction(dir1, self.config.line_width)
                    p2 = point.moved_direction(dir2, self.config.line_width)
                    self.tail.append(PathSegment(
                        self._line_drawable(p1, p2),
                        pos.time, self.config.tail_lag, self.config.colors))
                    pos.pos_tile.intersection_cnt += 1
                else:
                    self.tail.append(PathSegment(
                        self._line_drawable(point, point),
                        pos.time, self.config.tail_lag, self.config.colors))

    def __add_color_code(self, pos, time):
        pos.pos_tile.u_turn = False
        circle = Circle(pos.pos_tile.tile.get_middle(), self.config.line_width)
        code = UTurnCode(circle, time, self.config.tail_lag)
        self.tail.append(code)

    def __filter_tail(self, time):
        while len(self.tail) > 0 and not self.tail[0].is_valid(time):
            self.tail = self.tail[1:]

    def __update_tail(self, time):
        for p_drawable in self.tail:
            p_drawable.update(time)

    def __activate_tail(self):
        for p_drawable in self.tail:
            self.active_path.add_drawable(p_drawable.drawable)
