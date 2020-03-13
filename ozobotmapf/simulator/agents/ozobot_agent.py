import logging

from ozobotmapf.graphics.drawables import Line
from ozobotmapf.simulator.agents.agent import Agent
from ozobotmapf.simulator.path_position import PathPosition


class OzobotAgent(Agent):
    """
    This agent is animating it's path in time.
    """
    def __init__(self, agent_id, raw_plans, ozomap, config):
        super().__init__(agent_id, raw_plans, ozomap, config)
        self.max_time = self.__get_max_time()
        print(raw_plans)

    def update_path(self, time):
        self.active_path.clear()
        head = self.__get_position(time)
        tail = self.__get_position(time - self.config.tail_lag)

        self.__draw_test(head)
        self.__draw_test(tail)

    def __get_position(self, time):
        position = PathPosition(time, self.max_time)

        current_pos_id = self.__position_id_from_time(position.time)
        prev_t, curr_t, next_t = self.__get_tile_position_window(current_pos_id)
        position.set_position_window(prev_t, curr_t, next_t)

        enter, middle, leave = self.__time_window_from_position(current_pos_id)
        position.set_time_window(enter, middle, leave)

        return position

    def __position_id_from_time(self, time):
        """ Method returns a position ID in the path sequence of tiles based on current simulation time.

        Note:
            Because each tile middle has 'position in time' equal to (position_on_path * step_time)
            and step_time is the time of transfer between two tile middles, the round() operation will cover the
            possibility of the agent being in the first or second half of the tile.

        Args:
            time (int): Current simulation time (in milliseconds)

        Returns:
            int: Index in the path tile sequence (current tile position)
        """
        return round(time / self.config.step_time)

    def __time_window_from_position(self, pos_id):
        """Method computes expected entry, middle, and leave time for current position in path sequence.

        Note:
            Middle time is a simulation time when the agent is expected to stand exactly in the middle of the tile.
            Enter time is a simulation time when the agent is expected to enter given tile.
            Leave time is a simulation time when the agent is expected to leave given tile.

        Args:
            pos_id (int): Position index in the tile path sequence

        Returns:
            int: Expected time of entry in milliseconds
            int: Expected middle time in milliseconds
            int: Expected time of leave in milliseconds
        """
        middle_time = pos_id * self.config.step_time
        enter_time = middle_time - self.config.step_time / 2
        leave_time = middle_time + self.config.step_time / 2

        return enter_time, middle_time, leave_time

    def __get_tile_position_window(self, current_pos):
        current_tile = self.positions[current_pos]

        if current_pos == 0:
            previous_tile = current_tile
        else:
            previous_tile = self.positions[current_pos - 1]

        if current_pos + 1 >= len(self.positions):
            next_tile = current_tile
        else:
            next_tile = self.positions[current_pos + 1]

        return previous_tile, current_tile, next_tile

    def __draw_test(self, position):
        if position.is_first_half:
            enter, middle = position.curr_t.get_edge_middle(position.from_direction), position.curr_t.get_middle()
            position = enter.offset_to(middle, position.offset)
            self.active_path.add_drawable(
                Line(position, position, self.config.line_width)
            )
        else:
            middle, leave = position.curr_t.get_middle(), position.curr_t.get_edge_middle(position.to_direction)
            position = middle.offset_to(leave, position.offset)
            self.active_path.add_drawable(
                Line(position, position, self.config.line_width)
            )

    def __get_max_time(self):
        tmp_arr = [step for step in self.steps if step]
        last_step = tmp_arr[-1]
        real_len = len(self.steps) - self.steps[::-1].index(last_step)
        return self.config.step_time * real_len
