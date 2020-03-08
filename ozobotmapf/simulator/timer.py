import pygame


class Timer:
    def __init__(self):
        self.start_ticks = None
        self.finish_ticks = None

    def is_finished(self):
        return self.finish_ticks <= pygame.time.get_ticks()

    def start(self, length):
        self.start_ticks = pygame.time.get_ticks()
        self.finish_ticks = self.start_ticks + length

    def get_time(self):
        return pygame.time.get_ticks() - self.start_ticks
