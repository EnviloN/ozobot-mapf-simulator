from ozobotmapf.simulator.agents.agent import Agent
from ozobotmapf.simulator.agents.path_drawable import PathDrawable
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

        position = self._get_position(time)
        drawable = self.__create_drawable(position)
        if drawable:
            self.tail.append(drawable)

        self.__activate_tail()

    def __create_drawable(self, pos):
        if pos.pos_tile.type == PositionTypes.WAIT:
            return None
        else:
            if pos.pos_tile.is_turn:
                box_origin, s_angle, e_angle = pos.get_angle_from_position(self.config.tile_size, self.config.line_width)
                if box_origin:
                    return PathDrawable(self._arc_drawable(box_origin, s_angle, e_angle), pos.time, self.config.tail_lag)
                else:
                    return None
            else:
                point = pos.get_point_from_position()
                return PathDrawable(self._line_drawable(point, point), pos.time, self.config.tail_lag)

    def __filter_tail(self, time):
        while len(self.tail) > 0 and not self.tail[0].is_valid(time):
            self.tail = self.tail[1:]

    def __activate_tail(self):
        for p_drawable in self.tail:
            self.active_path.add_drawable(p_drawable.drawable)
