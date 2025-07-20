import pygame
from classs.Entity import Entity

class Wall(Entity):
    def __init__(self, start, end, color=(255,255,255)):
        self.start = start
        self.end = end
        self.color = color

    def draw(self, surface):
        pygame.draw.line(surface, self.color, self.start, self.end, 4)