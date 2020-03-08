import logging
import sys

import pygame

from ozobotmapf.graphics.ozomap_drawable import OzomapDrawableParser
from ozobotmapf.utils.constants import Colors, Values


class Simulator:
    def __init__(self, ozomap, plans, config):
        self.ozomap = ozomap
        self.plans = plans
        self.config = config

        self.agents = []
        self.map_objects = OzomapDrawableParser(ozomap, config).parse()

        self.__pygame_init()

    def __pygame_init(self):
        logging.info("Initializing pygame.")
        pygame.init()
        pygame.display.set_caption(Values.APP_NAME)
        self.__screen = None
        self.__width, self.__height = self.config.window_width, self.config.window_height

    def __init_screen(self):
        logging.info("Initializing screen.")
        if self.config.fullscreen:
            self.__screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        else:
            self.__screen = pygame.display.set_mode([self.config.window_width, self.config.window_height])
        self.__screen.fill(Colors.WHITE)
        self.__width, self.__height = pygame.display.get_surface().get_size()
        logging.debug("Application window resolution: {} x {} (px)".format(self.__width, self.__height))

    def run(self):
        logging.info("Starting the Simulator process.")
        self.__init_screen()

        self.__preview_map()
        self.wait_for_user()

        pygame.quit()
        logging.info("Successfully finished the Simulator process.")

    @staticmethod
    def wait_for_user():
        while True:
            for event in pygame.event.get():
                if (event.type == pygame.QUIT) or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                    logging.info("Quitting application.")
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    return

    def __draw_map(self, preview=False):
        self.__screen.fill(Colors.WHITE)

        if preview:
            self.map_objects[0].draw(self.__screen)  # Agent Starts/Ends

        if self.config.display_grid:
            self.map_objects[1].draw(self.__screen)  # Grid border lines

        if self.config.display_walls:
            self.map_objects[2].draw(self.__screen)  # Walls

        return self

    def __update(self):
        pygame.display.update()
        return self

    def __preview_map(self):
        self.__draw_map(True).__update()
