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
        self.preview = True

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
        self.__draw_map()

        self.wait()
        pygame.quit()
        logging.info("Successfully finished the Simulator process.")

    def wait(self):
        # TODO: Delete me when I'm not needed anymore.
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    logging.info("Quitting application.")
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:  # and event.key == K_ESCAPE:
                    return

    def __map_to_drawable(self):
        drawables = [self.__positions_to_drawable(), self.__borders_to_drawable()]
        return drawables

    def __draw_map(self):
        id_from = 0
        if not self.preview:
            id_from += 1

        self.__screen.fill(Colors.WHITE)
        for drawable in self.map_objects[id_from:]:
            drawable.draw(self.__screen)
        self.__update()

    def __update(self):
        pygame.display.update()
        return self
