from ozobotmapf.simulator.agents.agent import Agent


class OzobotAgent(Agent):
    """
    This agent is animating it's path in time, keeps Ozobot's limitations in mind, and uses Color Codes.
    Agent also supports curved paths.
    """
    def __init__(self, agent_id, raw_plans, ozomap, config):
        super().__init__(agent_id, raw_plans, ozomap, config)
        self.max_time = self.__get_max_time()

    def update_path(self, time):
        self.active_path.clear()

        head = self._get_position(time)
        tail = self._get_position(time - self.config.tail_lag)

    #     self.__build_active_path(tail, head)

    # def __build_active_path(self, from_pos, to_pos):
    #     if from_pos.curr_t == to_pos.curr_t:
    #         self.__build_same_tile_path(from_pos, to_pos)
    #     else:
    #         self.__build_different_tile_path(from_pos, to_pos)
