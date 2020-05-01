from ozobotmapf.simulator.agents.agent import Agent


class AnimatedAgent(Agent):
    """
    This agent is animating it's path in time.
    """
    def __init__(self, agent_id, raw_plans, ozomap, config):
        super().__init__(agent_id, raw_plans, ozomap, config)

    def update_path(self, time):
        self.active_path.clear()

        head = self._get_position(time)
        tail = self._get_position(time - self.config.tail_lag)

        self.__build_active_path(tail, head)

    def __build_active_path(self, from_pos, to_pos):
        if from_pos.curr_t == to_pos.curr_t:
            self.__build_same_tile_path(from_pos, to_pos)
        else:
            self.__build_different_tile_path(from_pos, to_pos)

    def __build_same_tile_path(self, from_pos, to_pos):
        if not self.config.curves:
            if from_pos.is_first_half == to_pos.is_first_half:
                self.__build_line_between(from_pos, to_pos)
            else:
                self.__build_line_to_middle(from_pos)
                self.__build_line_to_middle(to_pos)
        else:
            pass  # TODO: Support curved turns

    def __build_line_between(self, from_pos, to_pos):
        p_from = from_pos.get_point_from_position()
        p_to = to_pos.get_point_from_position()

        self._add_path_line(p_from, p_to)

    def __build_different_tile_path(self, from_pos, to_pos):
        if not self.config.curves:
            self.__build_line_before_leave(from_pos)
            self.__build_line_after_entry(to_pos)
        else:
            pass  # TODO: Support curved turns

    def __build_line_to_middle(self, pos):
        position = pos.get_point_from_position()
        middle = pos.curr_t.get_middle()

        self._add_path_line(middle, position)

    def __build_line_before_leave(self, from_pos):
        position = from_pos.get_point_from_position()
        leave = from_pos.curr_t.get_edge_middle(from_pos.to_direction)
        if from_pos.is_first_half:
            middle = from_pos.curr_t.get_middle()
            self._add_path_line(position, from_pos.curr_t.get_middle())
            self._add_path_line(middle, leave)
        else:
            self._add_path_line(position, leave)

    def __build_line_after_entry(self, to_pos):
        position = to_pos.get_point_from_position()
        enter = to_pos.curr_t.get_edge_middle(to_pos.from_direction)
        if to_pos.is_first_half:
            self._add_path_line(enter, position)
        else:
            middle = to_pos.curr_t.get_middle()
            self._add_path_line(middle, enter)
            self._add_path_line(middle, position)
