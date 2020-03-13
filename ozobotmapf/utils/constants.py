import pygame


class Colors:
    """Class contains color constants for easier use.

    Colors are represented as pygame.Color object.
    """
    WHITE = pygame.Color(255, 255, 255)
    BLACK = pygame.Color(0, 0, 0)
    GREY = pygame.Color(150, 150, 150)
    START = pygame.Color(230, 255, 230)
    FINISH = pygame.Color(255, 204, 204)


class Values:
    """Class contains global constants used across the application."""
    APP_NAME = "Ozobot MAPF Simulator"
    EDITOR_NAME = "Ozobot MAPF Map Editor"

    DISPLAY_CONFIGS_PATH = "../resources/config/display/"
    MAPS_PATH = "../resources/maps/"
    LOGS_PATH = "../resources/logs/"

    SIMULATOR_CONFIG = "../resources/config/simulator.ini"

    MAP_FILE_EXT = ".ozomap"


class Directions:
    """Class contains possible directions."""
    NONE = -1
    UP = 0
    RIGHT = 1
    DOWN = 2
    LEFT = 3


class AgentTypes:
    """Class contains supported agent types (classes)."""
    DUMMY = "dummy"
    OZOBOT = "ozobot"
