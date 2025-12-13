import pygame
import random
from src.core.settings import *

# Shapes
CIRCLE = "circle"
SQUARE = "square"
TRIANGLE = "triangle"

# Colors
COLORS = [RED, BLUE, GREEN, (255, 255, 0), (0, 255, 255), (255, 0, 255)]


class Target:
    def __init__(
        self, x, y, radius, lifetime=DEFAULT_TARGET_LIFETIME, dx=0, dy=0, shape=CIRCLE
    ):
        self.x = x
        self.y = y
        self.radius = radius
        self.lifetime = lifetime
        self.spawn_time = pygame.time.get_ticks()
        self.color = random.choice(COLORS)
        self.shape = shape
        self.dx = dx
        self.dy = dy
        self.active = True

    def update(self):
        current_time = pygame.time.get_ticks()
        if current_time - self.spawn_time > self.lifetime:
            self.active = False  # Expired
            return

        # Movement
        self.x += self.dx
        self.y += self.dy

        # Bounce off walls (optional, or just go off screen)
        if self.x < self.radius or self.x > SCREEN_WIDTH - self.radius:
            self.dx *= -1
        if self.y < self.radius or self.y > SCREEN_HEIGHT - self.radius:
            self.dy *= -1

    def draw(self, surface):
        if not self.active:
            return

        if self.shape == CIRCLE:
            pygame.draw.circle(
                surface, self.color, (int(self.x), int(self.y)), self.radius
            )
        elif self.shape == SQUARE:
            rect = pygame.Rect(
                self.x - self.radius,
                self.y - self.radius,
                self.radius * 2,
                self.radius * 2,
            )
            pygame.draw.rect(surface, self.color, rect)
        elif self.shape == TRIANGLE:
            points = [
                (self.x, self.y - self.radius),
                (self.x - self.radius, self.y + self.radius),
                (self.x + self.radius, self.y + self.radius),
            ]
            pygame.draw.polygon(surface, self.color, points)

    def check_collision(self, mouse_x, mouse_y):
        if not self.active:
            return False

        if self.shape == CIRCLE:
            distance = ((mouse_x - self.x) ** 2 + (mouse_y - self.y) ** 2) ** 0.5
            return distance <= self.radius
        elif self.shape == SQUARE:
            return (self.x - self.radius <= mouse_x <= self.x + self.radius) and (
                self.y - self.radius <= mouse_y <= self.y + self.radius
            )
        elif self.shape == TRIANGLE:
            # Simplified collision for triangle (bounding box for now to keep it fast)
            return (self.x - self.radius <= mouse_x <= self.x + self.radius) and (
                self.y - self.radius <= mouse_y <= self.y + self.radius
            )


class StaticTarget(Target):
    def __init__(self, x, y, radius, lifetime):
        super().__init__(
            x,
            y,
            radius,
            lifetime,
            dx=0,
            dy=0,
            shape=random.choice([CIRCLE, SQUARE, TRIANGLE]),
        )


class MovingTarget(Target):
    def __init__(self, x, y, radius, lifetime, speed=2):
        dx = random.choice([-speed, speed]) * random.random()
        dy = random.choice([-speed, speed]) * random.random()
        super().__init__(
            x,
            y,
            radius,
            lifetime,
            dx,
            dy,
            shape=random.choice([CIRCLE, SQUARE, TRIANGLE]),
        )
