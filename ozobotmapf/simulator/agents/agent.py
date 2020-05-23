import logging

from ozobotmapf.graphics.drawables import FullArrow, DrawableGroup, Line, Arc
from ozobotmapf.graphics.shapes import Rectangle
from ozobotmapf.simulator.path_position import PathPosition
from ozobotmapf.simulator.position_tile import PositionTile
from ozobotmapf.utils.constants import Directions


class Agent:
    def __init__(self, agent_id, raw_plans, ozomap, config):
        logging.info("Initializing agent {}.".format(agent_id))
        logging.debug("Agent {} plan: {}".format(agent_id, raw_plans))

        self.id = agent_id
        self.ozomap = ozomap
        self.config = config

        self.raw_positions = raw_plans['pos_list']
        self.raw_steps = raw_plans['steps']

        self.__trim_positions()
        self.plan_length = len(self.raw_positions) - 1
        self.max_time = self.__get_max_time()

        self.positions = self.__tiles_from_positions()
        self.steps = self.__tiles_from_steps()

        self.active_path = DrawableGroup()
        self.direction_arrow = self.__create_direction_arrow()

    def update_path(self, time):
        pass

    def get_active_path(self):
        return self.active_path

    def __tiles_from_positions(self):
        tiles = [self.ozomap.get_tile_by_id(raw_id) for raw_id in self.raw_positions]
        positions = []
        for i in range(len(tiles)):
            current_tile = tiles[i]
            previous_tile = tiles[i-1] if i != 0 else tiles[i]
            next_tile = tiles[i+1] if i != len(tiles) - 1 else tiles[i]

            from_direction = current_tile.direction_to(previous_tile)
            to_direction = current_tile.direction_to(next_tile)

            position = PositionTile(current_tile, from_direction, to_direction)
            if i != 0 and i != len(tiles) - 1:
                previous_direction = self.__direction_look_back(tiles, i)
                next_direction = self.__direction_look_ahead(tiles, i)
                position.set_movement_directions(previous_direction, next_direction)

            positions.append(position)

        return positions

    @staticmethod
    def __direction_look_back(tiles, index):
        direction = Directions.NONE
        tile = tiles[index]
        while direction == Directions.NONE and index >= 0:
            direction = tile.direction_to(tiles[index])
            index -= 1
        return direction

    @staticmethod
    def __direction_look_ahead(tiles, index):
        direction = Directions.NONE
        tile = tiles[index]
        while direction == Directions.NONE and index <= len(tiles) - 1:
            direction = tile.direction_to(tiles[index])
            index += 1
        return direction

    def __tiles_from_steps(self):
        steps = []
        for step in self.raw_steps:
            if step is None:
                steps.append(None)
            else:
                t_from = self.ozomap.get_tile_by_id(step[0])
                t_to = self.ozomap.get_tile_by_id(step[1])
                steps.append((t_from, t_to))
        return steps

    def __create_direction_arrow(self):
        for step in self.steps:
            if step is not None:
                direction = step[0].direction_to(step[1])
                position = step[0].get_edge_middle(direction)
                return FullArrow(position, direction, self.config.wall_width)
        return None

    def _get_position(self, time):
        position = PathPosition(time, self.max_time)

        current_pos_id = self.__position_id_from_time(position.time)
        current_pos = self.positions[current_pos_id]
        next_pos = self.positions[current_pos_id + 1] if current_pos_id < len(self.positions) - 1 else current_pos
        prev_pos = self.positions[current_pos_id - 1] if current_pos_id > 0 else current_pos
        position.set_position_tile(current_pos, next_pos, prev_pos)

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

    def __get_max_time(self):
        """Method computes the time until the last step."""
        return self.config.step_time * self.plan_length

    def __trim_positions(self):
        tmp_arr = [step for step in self.raw_steps if step]
        last_step = tmp_arr[-1]
        real_len = len(self.raw_steps) - self.raw_steps[::-1].index(last_step) + 1
        self.raw_positions = self.raw_positions[:real_len]

    def _line_drawable(self, p_from, p_to):
        return Line(p_from, p_to, self.config.line_width)

    def _arc_drawable(self, box_origin, start, end):
        box_size = self.config.tile_size + self.config.line_width
        box = Rectangle(box_origin, box_size, box_size)
        return Arc(box, start, end, self.config.line_width)
