import pygame
import random
from src.core.settings import *


class Target:
    def __init__(self, x, y, radius, lifetime=DEFAULT_TARGET_LIFETIME):
        self.x = x
        self.y = y
        self.radius = radius
        self.lifetime = lifetime
        self.spawn_time = pygame.time.get_ticks()
        self.color = RED
        self.active = True

    def update(self):
        current_time = pygame.time.get_ticks()
        if current_time - self.spawn_time > self.lifetime:
            self.active = False  # Expired

    def draw(self, surface):
        if self.active:
            pygame.draw.circle(
                surface, self.color, (int(self.x), int(self.y)), self.radius
            )

    def check_collision(self, mouse_x, mouse_y):
        if not self.active:
            return False
        distance = ((mouse_x - self.x) ** 2 + (mouse_y - self.y) ** 2) ** 0.5
        return distance <= self.radius


class StaticTarget(Target):
    def __init__(self, x, y, radius, lifetime):
        super().__init__(x, y, radius, lifetime)
        self.color = RED
