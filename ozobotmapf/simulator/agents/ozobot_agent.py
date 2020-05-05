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
        self.__add_drawables(position)

        if position.pos_tile.u_turn and not position.is_first_half:
            self.__add_color_code(position, time)

        self.__activate_tail()

    def __add_drawables(self, pos):
        if pos.pos_tile.type != PositionTypes.WAIT:
            if pos.pos_tile.is_turn and not (pos.pos_tile.type == PositionTypes.STOP):
                box_origin, s_angle, e_angle = pos.get_angle_from_position(self.config.tile_size, self.config.line_width)
                if box_origin:
                    self.tail.append(TurnSegment(
                        self._arc_drawable(box_origin, s_angle, e_angle),
                        pos.time, self.config.tail_lag, self.config.colors)
                    )
            else:
                point = pos.get_point_from_position(True)
                if self.config.colors and pos.should_print_intersection():
                    dir1, dir2 = pos.get_normal_directions()
                    p1 = point.moved_direction(dir1, self.config.line_width)
                    p2 = point.moved_direction(dir2, self.config.line_width)
                    if pos.next_pos_tile.is_turn and not pos.is_first_half:
                        segments = [TurnSegment(
                            self._line_drawable(p1, p2),
                            pos.time, self.config.tail_lag, self.config.colors),
                            TurnSegment(
                                self._line_drawable(point, point.moved_direction(pos.pos_tile.from_dir, 15)),
                                pos.time, self.config.tail_lag, self.config.colors)
                        ]
                    else:
                        segments = [PathSegment(
                            self._line_drawable(p1, p2),
                            pos.time, self.config.tail_lag, self.config.colors),
                            PathSegment(
                                self._line_drawable(point, point.moved_direction(pos.pos_tile.from_dir, 15)),
                                pos.time, self.config.tail_lag, self.config.colors)
                        ]
                    for segment in segments:
                        self.tail.append(segment)
                    pos.pos_tile.intersection_cnt += 1
                else:
                    if not (pos.pos_tile.type == PositionTypes.STOP and pos.pos_tile.is_turn):
                        if pos.next_pos_tile.is_turn and not pos.is_first_half and pos.offset >= 0.65:
                            segments = [TurnSegment(
                                self._line_drawable(point, point),
                                pos.time, self.config.tail_lag, self.config.colors)]
                        else:
                            segments = [PathSegment(
                                self._line_drawable(point, point),
                                pos.time, self.config.tail_lag, self.config.colors)]

                        for segment in segments:
                            self.tail.append(segment)
                    else:
                        entry = pos.pos_tile.tile.get_edge_middle(pos.pos_tile.previous_direction)
                        leave = pos.pos_tile.tile.get_edge_middle(pos.pos_tile.next_direction)
                        p = pos.pos_tile.tile.get_middle().moved_direction(pos.pos_tile.next_direction, self.config.tile_size / 3)
                        self.tail.append(PathSegment(
                            self._line_drawable(entry, entry.offset_to(p, 0.5)),
                            pos.time, self.config.tail_lag, self.config.colors))

    def __add_color_code(self, pos, time):
        pos.pos_tile.u_turn = False
        circle = Circle(pos.pos_tile.tile.get_middle(), self.config.color_code_radius)
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
