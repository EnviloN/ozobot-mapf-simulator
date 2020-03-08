from ozobotmapf.utils.constants import Directions
from ozobotmapf.graphics.drawables import FullArrow


class Agent:
    def __init__(self, agent_id, raw_plans, ozomap, config):
        self.id = agent_id
        self.ozomap = ozomap
        self.config = config

        self.raw_positions = raw_plans['pos_list']
        self.raw_steps = raw_plans['steps']
        self.positions = self.__tiles_from_positions()
        self.steps = self.__tiles_from_steps()

        self.active_path = set()
        self.direction_arrow = self.__create_direction_arrow()

    def update(self):
        pass

    def get_active_path(self):
        return self.active_path

    def __tiles_from_positions(self):
        return [self.ozomap.get_tile_by_id(tile_id) for tile_id in self.raw_positions]

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
                position = self.__get_direction_arrow_position(step[0], direction)
                return FullArrow(position, direction, self.config.wall_width)
        return None

    def __get_direction_arrow_position(self, tile, direction):
        size = self.config.tile_size
        half = size / 2
        if direction == Directions.UP:
            return tile.origin.moved(half, 0)
        elif direction == Directions.RIGHT:
            return tile.origin.moved(size, half)
        elif direction == Directions.DOWN:
            return tile.origin.moved(half, size)
        elif direction == Directions.LEFT:
            return tile.origin.moved(0, half)