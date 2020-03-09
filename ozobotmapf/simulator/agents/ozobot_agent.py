import math

from ozobotmapf.graphics.drawables import Line
from ozobotmapf.simulator.agents.agent import Agent


class OzobotAgent(Agent):
    def __init__(self, agent_id, raw_plans, ozomap, config):
        super().__init__(agent_id, raw_plans, ozomap, config)
        print(raw_plans)

    def update_path(self, time):
        self.active_path.clear()

        current_pos = self.__position_id_from_time(time)
        if current_pos >= len(self.positions):
            return

        prev_t, curr_t, next_t = self.__get_tile_position_window(current_pos)

        middle_time = current_pos * self.config.step_time
        enter_time = middle_time - self.config.step_time / 2
        leave_time = middle_time + self.config.step_time / 2

        if enter_time <= time < middle_time:  # First half
            offset = (time - enter_time) / (middle_time - enter_time)
            from_direction = curr_t.direction_to(prev_t)
            if from_direction is not None:
                enter, middle = curr_t.get_edge_middle(from_direction), curr_t.get_middle()
                position = enter.offset_to(middle, offset)
                self.active_path.add_drawable(
                    Line(position, position, self.config.line_width)
                )
        else:  # Second half
            offset = (time - middle_time) / (leave_time - middle_time)
            to_direction = curr_t.direction_to(next_t)
            if to_direction is not None:
                middle, leave = curr_t.get_middle(), curr_t.get_edge_middle(to_direction)
                position = middle.offset_to(leave, offset)
                self.active_path.add_drawable(
                    Line(position, position, self.config.line_width)
                )

    def old_update_path(self, time):
        self.active_path.clear()

        current_pos = self.__position_id_from_time(time)
        if current_pos >= len(self.positions):
            return

        prev_t, curr_t, next_t = self.__get_tile_position_window(current_pos)
        self.__build_active_path(prev_t, curr_t, next_t)

    def __position_id_from_time(self, time):
        return round(time / self.config.step_time)

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

    def __build_active_path(self, prev_t, curr_t, next_t):
        from_direction = curr_t.direction_to(prev_t)
        if from_direction is not None:
            self.active_path.add_drawable(
                Line(curr_t.get_middle(), curr_t.get_edge_middle(from_direction), self.config.line_width)
            )

        to_direction = curr_t.direction_to(next_t)
        if to_direction is not None:
            self.active_path.add_drawable(
                Line(curr_t.get_middle(), curr_t.get_edge_middle(to_direction), self.config.line_width)
            )
