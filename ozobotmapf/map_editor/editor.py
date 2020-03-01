import logging
import math
import os
import re

import pygame
import enum
from pygame.locals import *
import heapq

from ozobotmapf.graphics.point import Point
from ozobotmapf.map_editor.EditorException import EditorException
from ozobotmapf.utils.constants import Colors, Values


class Mode(enum.Enum):
    WALL = 1
    START = 2
    FINISH = 3


class Editor:

    def __init__(self, ozomap, config):
        self.config = config
        self.ozomap = ozomap

        self.mode = Mode.WALL
        self.starts, self.ends = [], []
        self.click_tolerance = config.line_width
        self.__pygame_init()

    def __pygame_init(self):
        logging.info("Initializing pygame.")
        pygame.init()
        pygame.display.set_caption(Values.EDITOR_NAME)
        self.__screen = None
        self.__width, self.__height = self.config.window_width, self.config.window_height
        self.font = pygame.font.Font('freesansbold.ttf', 20)

    def __init_screen(self):
        logging.info("Initializing screen.")
        if self.config.fullscreen:
            self.__screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        else:
            self.__screen = pygame.display.set_mode([self.config.window_width, self.config.window_height])
        self.__screen.fill(Colors.WHITE)
        self.__width, self.__height = pygame.display.get_surface().get_size()
        logging.debug("Application window resolution: {} x {} (px)".format(self.__width, self.__height))

    def __update(self):
        pygame.display.update()
        return self

    def run(self):
        logging.info("Starting the Map Editor process.")
        self.__greet_user()
        self.__get_map_attributes_from_user()
        self.ozomap.init_empty_map(self.config)

        self.__init_screen()
        self.__draw_map()

        save = self.__game_loop()
        pygame.quit()

        if save:
            self.__save_map()
        logging.info("Successfully finished the Map Editor process.")

    @staticmethod
    def __greet_user():
        print("\n\nWelcome to the '{}'!".format(Values.EDITOR_NAME))

    def __get_map_attributes_from_user(self):
        print("Please define the following attributes for your new level:")
        self.__get_map_width_from_user()
        self.__get_map_height_from_user()
        self.__get_map_agent_cnt_from_user()

        self.starts = list(range(1, self.config.map_agent_count + 1))
        self.ends = list(range(1, self.config.map_agent_count + 1))

    def __get_map_width_from_user(self):
        valid = False
        width = 0
        while not valid:
            try:
                width = int(input("Map Width (max {}): ".format(self.config.max_map_width)))
                if 0 < width <= self.config.max_map_width:
                    valid = True
                else:
                    print("Map width needs to be between 1 and {} (the maximum you can fit on your display)!"
                          .format(self.config.max_map_width))
            except ValueError:
                print("Map width needs to be an integer!")
        self.config.map_width = width

    def __get_map_height_from_user(self):
        valid = False
        height = 0
        while not valid:
            try:
                height = int(input("Map Height (max {}): ".format(self.config.max_map_height)))
                if 0 < height <= self.config.max_map_height:
                    valid = True
                else:
                    print("Map height needs to be between 1 and {} (the maximum you can fit on your display)!"
                          .format(self.config.max_map_height))
            except ValueError:
                print("Map height needs to be an integer!")
        self.config.map_height = height

    def __get_map_agent_cnt_from_user(self):
        valid = False
        agent_cnt = 0
        max_agent_cnt = self.config.map_width * self.config.map_height
        while not valid:
            try:
                agent_cnt = int(input("Map Agent Count (max {}): ".format(max_agent_cnt)))
                if 0 < agent_cnt <= max_agent_cnt:
                    valid = True
                else:
                    print("Map agent count needs to be between 1 and {} (the maximum you can fit on your display)!"
                          .format(max_agent_cnt))
            except ValueError:
                print("Map agent count needs to be an integer!")
        self.config.map_agent_count = agent_cnt

    def __draw_map(self):
        self.__screen.fill(Colors.WHITE)
        self.__draw_tiles()
        self.__draw_walls()
        self.__update()

    def __draw_tiles(self):
        for x in range(len(self.ozomap.grid)):
            for y in range(len(self.ozomap.grid[0])):
                self.__draw_tile(self.ozomap.grid[x][y])

    def __draw_tile(self, tile):
        tile_size = self.config.tile_size
        if tile.start_agent > 0 and tile.finish_agent > 0:
            self.__draw_double_color_tile(tile, 10)
            self.__render_text_in_tile(tile, "S: {} / F: {}".format(tile.start_agent, tile.finish_agent))
        elif tile.start_agent > 0:
            self.__screen.fill(Colors.START, [tile.origin.x, tile.origin.y, tile_size, tile_size])
            self.__render_text_in_tile(tile, "S: {}".format(tile.start_agent))
        elif tile.finish_agent > 0:
            self.__screen.fill(Colors.FINISH, [tile.origin.x, tile.origin.y, tile_size, tile_size])
            self.__render_text_in_tile(tile, "F: {}".format(tile.finish_agent))

        pygame.draw.rect(self.__screen, Colors.GREY, [tile.origin.x, tile.origin.y, tile_size, tile_size],
                         self.config.tile_border_width)

    def __draw_double_color_tile(self, tile, splits):
        colors = [Colors.START, Colors.FINISH]
        current_color = 0
        tile_size = self.config.tile_size
        part_size = tile_size / splits
        for part_x in range(splits):
            for part_y in range(splits):
                x = tile.origin.x + part_x * part_size
                y = tile.origin.y + part_y * part_size
                self.__screen.fill(colors[current_color], [x, y, part_size, part_size])
                current_color = 1 - current_color
            current_color = 1 - current_color

    def __render_text_in_tile(self, tile, text):
        text = self.font.render(text, True, Colors.BLACK)
        text_rect = text.get_rect()
        half_size = self.config.tile_size / 2
        text_rect.center = (tile.origin.x + half_size, tile.origin.y + half_size)
        self.__screen.blit(text, text_rect)

    def __draw_walls(self):
        for x in range(len(self.ozomap.grid)):
            for y in range(len(self.ozomap.grid[0])):
                tile = self.ozomap.grid[x][y]
                if tile.has_upper_wall():
                    self.__draw_upper_wall(tile.origin)
                if tile.has_right_wall():
                    self.__draw_right_wall(tile.origin)
                if tile.has_bottom_wall():
                    self.__draw_bottom_wall(tile.origin)
                if tile.has_left_wall():
                    self.__draw_left_wall(tile.origin)

    def __draw_upper_wall(self, tile_origin):
        """Method draws upper wall of a tile.

        Args:
            tile_origin (Point): Origin of a given tile
        """
        self.__draw_wall_line(tile_origin,
                              tile_origin.moved(self.config.tile_size, 0))

    def __draw_right_wall(self, tile_origin):
        """Method draws right wall of a tile.

        Args:
            tile_origin (Point): Origin of a given tile
        """
        self.__draw_wall_line(tile_origin.moved(self.config.tile_size, 0),
                              tile_origin.moved(self.config.tile_size, self.config.tile_size))

    def __draw_bottom_wall(self, tile_origin):
        """Method draws bottom wall of a tile.

        Args:
            tile_origin (Point): Origin of a given tile
        """
        self.__draw_wall_line(tile_origin.moved(self.config.tile_size, self.config.tile_size),
                              tile_origin.moved(0, self.config.tile_size))

    def __draw_left_wall(self, tile_origin):
        """Method draws left wall of a tile.

        Args:
            tile_origin (Point): Origin of a given tile
        """
        self.__draw_wall_line(tile_origin.moved(0, self.config.tile_size),
                              tile_origin)

    def __draw_wall_line(self, start, end):
        """Method draws a wall line from start to end.

        Note:
            Line width can be configured in the configuration file.

        Args:
            start (Point): Start point of the line
            end (Point): End point of the line
        """
        pygame.draw.line(self.__screen, Colors.BLACK, start, end, self.config.wall_width)

    def __game_loop(self):
        end, save = False, False
        while not end:
            for event in pygame.event.get():
                if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                    logging.info("Quitting Map Editor.")
                    end = True
                if event.type == KEYDOWN and event.key == K_RETURN:
                    if len(self.starts) == 0 and len(self.ends) == 0:
                        logging.info("Quitting Map Editor and Saving level.")
                        end, save = True, True
                    else:
                        print("You have to put dawn all agent starts and agent ends.")
                if event.type == KEYDOWN and event.key == K_w:
                    self.mode = Mode.WALL
                if event.type == KEYDOWN and event.key == K_s:
                    self.mode = Mode.START
                if event.type == KEYDOWN and event.key == K_f:
                    self.mode = Mode.FINISH
                if event.type == MOUSEBUTTONUP:
                    x, y = pygame.mouse.get_pos()
                    self.__handle_mouse_click(Point(x, y))

        return save

    def __handle_mouse_click(self, pos):
        if self.mode == Mode.WALL:
            self.__handle_wall_toggle(pos)
        elif self.mode == Mode.START or self.mode == Mode.FINISH:
            self.__handle_tile_toggle(pos)
        else:
            raise EditorException("Invalid editor mode!")

        self.__draw_map()

    def __handle_wall_toggle(self, pos):
        if self.__is_pos_on_border(pos):
            for x in range(self.config.map_width):
                for y in range(self.config.map_height):
                    self.__toggle_tile_walls_if_hit(self.ozomap.grid[x][y], pos)

    def __is_pos_on_border(self, pos):
        origin = self.ozomap.origin

        for ith_col in range(1, self.config.map_width):
            x_border = origin.x + ith_col * self.config.tile_size
            x_from, x_to = x_border - self.click_tolerance, x_border + self.click_tolerance
            if x_from <= pos.x <= x_to:
                return True

        for ith_row in range(1, self.config.map_height):
            y_border = origin.y + ith_row * self.config.tile_size
            y_from, y_to = y_border - self.click_tolerance, y_border + self.click_tolerance
            if y_from <= pos.y <= y_to:
                return True

        return False

    def __toggle_tile_walls_if_hit(self, tile, pos):
        xp, yp = pos.x, pos.y
        xo, yo = tile.origin.x, tile.origin.y
        t, ts = self.click_tolerance, self.config.tile_size
        if (yo-t <= yp <= yo+t) and (xo+t <= xp <= xo+ts-t):
            tile.walls[0] = not tile.walls[0]
        if (xo+ts-t <= xp <= xo+ts+t) and (yo+t <= yp <= yo+ts-t):
            tile.walls[1] = not tile.walls[1]
        if (yo+ts-t <= yp <= yo+ts+t) and (xo+t <= xp <= xo+ts-t):
            tile.walls[2] = not tile.walls[2]
        if (xo-t <= xp <= xo+t) and (yo+t <= yp <= yo+ts-t):
            tile.walls[3] = not tile.walls[3]

    def __handle_tile_toggle(self, pos):
        tile = self.__get_tile_from_position(pos)
        if tile is not None:
            if self.mode == Mode.START:
                self.__handle_tile_start_toggle(tile)
            elif self.mode == Mode.FINISH:
                self.__handle_tile_finish_toggle(tile)

    def __get_tile_from_position(self, pos):
        x = math.floor((pos.x - self.ozomap.origin.x) / self.config.tile_size)
        y = math.floor((pos.y - self.ozomap.origin.y) / self.config.tile_size)
        if 0 <= x < self.config.map_width and 0 <= y < self.config.map_height:
            return self.ozomap.grid[x][y]
        else:
            return None

    def __handle_tile_start_toggle(self, tile):
        if tile.start_agent > 0:
            if tile.start_agent in self.starts:
                raise EditorException("Agent Starts contains already placed start.")
            heapq.heappush(self.starts, tile.start_agent)
            tile.start_agent = 0
        else:
            if len(self.starts) > 0:
                tile.start_agent = heapq.heappop(self.starts)

    def __handle_tile_finish_toggle(self, tile):
        if tile.finish_agent > 0:
            if tile.finish_agent in self.ends:
                raise EditorException("Agent Starts contains already placed start.")
            heapq.heappush(self.ends, tile.finish_agent)
            tile.finish_agent = 0
        else:
            if len(self.ends) > 0:
                tile.finish_agent = heapq.heappop(self.ends)

    def __save_map(self):
        map_name = self.__get_map_name_from_user()
        self.__save_to_file(map_name)

    def __get_map_name_from_user(self):
        name = ""
        valid = False
        while not valid:
            automatic_name = self.__generate_automatic_map_name()
            name = input("Enter new level name [{}]: ".format(automatic_name))
            name = automatic_name if name == "" else name
            if os.path.isfile(Values.MAPS_PATH + name + Values.MAP_FILE_EXT):
                print("A level with this name already exists in '{}'!".format(Values.MAPS_PATH))
                continue
            if not self.__valid_attributes_in_map_name(name):
                print("It is advised that the level name has at least 3 numbers. "
                      "First three numbers should be correct level attributes (in this case: {}, {}, {})."
                      .format(self.config.map_width, self.config.map_height, self.config.map_agent_count))
                answer = ""
                while answer != 'y' or answer != 'n':
                    answer = input("Are you sure you want to use level name '{}'? (y/n): ".format(name)).lower()
                if answer == 'y':
                    valid = True
            else:
                valid = True
        return name

    def __generate_automatic_map_name(self):
        suffix = 1
        name = "{}x{}_{}a".format(self.config.map_width, self.config.map_height, self.config.map_agent_count)

        if not os.path.isfile(Values.MAPS_PATH + name + Values.MAP_FILE_EXT):
            return name

        while os.path.isfile(Values.MAPS_PATH + name + Values.MAP_FILE_EXT):
            name = "{}x{}_{}a_{}".format(self.config.map_width, self.config.map_height,
                                         self.config.map_agent_count, suffix)
            suffix += 1
        return name

    def __valid_attributes_in_map_name(self, name):
        numbers = [int(x) for x in re.findall(r'\d+', name)]
        attributes = [self.config.map_width, self.config.map_height, self.config.map_agent_count]
        if len(numbers) < 3:
            return False
        if numbers[0] != attributes[0] or numbers[1] != attributes[1] or numbers[2] != attributes[2]:
            return False
        return True

    def __save_to_file(self, name):
        lines = ["V =\n"]
        tile_id = 0
        for x in range(self.config.map_height):
            for y in range(self.config.map_width):
                tile = self.ozomap.grid[y][x]
                lines.append("({},{},{})\n".format(tile_id, tile.start_agent, tile.finish_agent))
                tile_id += 1
        lines.append("E =\n")
        tile_id = 0
        for x in range(self.config.map_height):
            for y in range(self.config.map_width):
                if not self.ozomap.grid[y][x].walls[2]:
                    lines.append("{" + "{},{}".format(tile_id, tile_id + self.config.map_width) + "}\n")
                if not self.ozomap.grid[y][x].walls[1]:
                    lines.append("{" + "{},{}".format(tile_id, tile_id + 1) + "}\n")
                tile_id += 1

        with open(Values.MAPS_PATH + name + Values.MAP_FILE_EXT, "w") as file:
            file.writelines(lines)
