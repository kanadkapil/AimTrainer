import pygame
from src.core.settings import *


class HUD:
    def __init__(self):
        self.font = pygame.font.SysFont("Arial", 24)

    def draw(self, surface, score, lives):
        # Score
        score_surf = self.font.render(f"Score: {score}", True, WHITE)
        surface.blit(score_surf, (20, 20))

        # Lives
        lives_surf = self.font.render(f"Lives: {lives}", True, RED)
        surface.blit(lives_surf, (20, 60))

        # Dynamic Crosshair
        mouse_pos = pygame.mouse.get_pos()
        pygame.draw.circle(surface, GREEN, mouse_pos, 5, 1)
