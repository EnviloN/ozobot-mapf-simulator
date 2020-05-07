import pygame


class Timer:
    DEBUG_SPEED = 50  # How much milliseconds time advances by each game loop.

    def __init__(self, debug=False):
        self.start_ticks = None
        self.finish_ticks = None
        self.ticks = 0
        self.debug = debug

    def is_finished(self):
        if not self.debug:
            return self.finish_ticks <= pygame.time.get_ticks()
        else:
            return self.finish_ticks <= self.ticks

    def start(self, length):
        if not self.debug:
            self.start_ticks = pygame.time.get_ticks()
        else:
            self.start_ticks = 0

        self.finish_ticks = self.start_ticks + length

    def get_time(self):
        if self.debug:
            self.ticks += self.DEBUG_SPEED
            return self.ticks
        else:
            return pygame.time.get_ticks() - self.start_ticks
