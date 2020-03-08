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

        self.map_objects = OzomapDrawableParser(ozomap, config).parse()
        self.agents = self.__init_agents()

        self.__pygame_init()

    def __init_agents(self):
        agents = []
        for agent_id in self.plans:
            agents.append(self.config.agent_class(agent_id, self.plans[agent_id], self.ozomap, self.config))

        return agents

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

        self.__update_agents()
        self.__draw_active_paths().__update()

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

    def __draw_all_paths(self):
        for agent in self.agents:
            self.__draw_agent_path(agent)

    def __draw_agent_path(self, agent):
        for drawable in agent.get_active_path():
            drawable.draw(self.__screen)

    def __update(self):
        pygame.display.update()
        return self

    def __preview_map(self):
        self.__draw_map(True)

        if self.config.direction_preview:
            for agent in self.agents:
                if agent.direction_arrow is not None:
                    agent.direction_arrow.draw(self.__screen)

        self.__update()

    def __update_agents(self):
        for agent in self.agents:
            agent.update_path()

    def __draw_active_paths(self):
        for agent in self.agents:
            agent.get_active_path().draw(self.__screen)
        return self
