import pygame
from src.core.settings import *


class HUD:
    def __init__(self):
        self.font = pygame.font.SysFont("Arial", 24)
        self.score_text = ""

    def draw(self, surface, score, time_left=None):
        # Score
        score_surf = self.font.render(f"Score: {score}", True, WHITE)
        surface.blit(score_surf, (20, 20))

        # Time (if applicable)
        if time_left is not None:
            time_surf = self.font.render(f"Time: {int(time_left)}s", True, WHITE)
            surface.blit(time_surf, (SCREEN_WIDTH - 150, 20))

        # Crosshair (optional, maybe distinct from HUD?)
        mouse_pos = pygame.mouse.get_pos()
        pygame.draw.circle(surface, GREEN, mouse_pos, 5, 1)
