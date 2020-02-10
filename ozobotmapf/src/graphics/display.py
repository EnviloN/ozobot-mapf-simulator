import logging
import pygame

from src.utils.constants import Colors


class Display:
    def __init__(self, resolution, fullscreen):
        logging.info("Initialising pygame and display.")
        pygame.init()
        self.screen = pygame.display.set_mode((0,0), pygame.FULLSCREEN) if fullscreen else \
            pygame.display.set_mode(resolution)
        self.screen.fill(Colors.WHITE)
        pygame.display.update()

        self.width, self.height = pygame.display.get_surface().get_size()
        logging.debug("Application resolution: {} x {} (px)".format(self.width, self.height))