import random
import pygame
from src.core.settings import *
from .targets import StaticTarget
from src.data.logger import DataLogger
from src.ai.agent import AIAgent


class GameMode:
    def __init__(self):
        self.targets = []
        self.score = 0
        self.last_spawn_time = 0

        # AI & Data
        self.logger = DataLogger()
        self.agent = AIAgent()

        # Dynamic Parameters
        self.spawn_rate = TARGET_SPAWN_RATE
        self.current_target_size = DEFAULT_TARGET_SIZE

    def update(self):
        current_time = pygame.time.get_ticks()

        # Spawn new targets
        if current_time - self.last_spawn_time > self.spawn_rate:
            self.spawn_target()
            self.last_spawn_time = current_time

        # Update existing targets
        for target in self.targets:
            target.update()

        # Remove inactive targets
        # Log missed targets if they expired naturally (not clicked)
        active_targets = []
        for t in self.targets:
            if t.active:
                active_targets.append(t)
            else:
                # If it wasn't clicked (we assume it expired if we are removing it here and it wasn't flagged as hit earlier?
                # Actually handle_click sets active=False. We need to distinguish expiration vs hit.
                # For now, let's just clean up.
                pass
        self.targets = active_targets

    def draw(self, surface):
        for target in self.targets:
            target.draw(surface)

    def handle_click(self, pos):
        hit = False
        click_time = pygame.time.get_ticks()

        for target in self.targets:
            if target.check_collision(pos[0], pos[1]):
                target.active = False  # Remove target
                self.score += 1
                hit = True

                # Calculate reaction time (simplified: time since spawn)
                reaction_time = click_time - target.spawn_time
                self.logger.log_event("HIT", pos[0], pos[1], f"time={reaction_time}ms")

                # AI Analysis
                new_params = self.agent.analyze_performance(True, reaction_time)
                self.apply_params(new_params)

                break

        if not hit:
            self.logger.log_event("MISS", pos[0], pos[1])
            new_params = self.agent.analyze_performance(
                False, 0
            )  # 0 ms reaction time for miss? Or just ignore time.
            self.apply_params(new_params)

        return hit

    def apply_params(self, params):
        if "spawn_rate" in params:
            self.spawn_rate = params["spawn_rate"]
        if "target_size" in params:
            self.current_target_size = params["target_size"]

    def spawn_target(self):
        pass  # To be implemented by subclasses


class FlickMode(GameMode):
    def spawn_target(self):
        size = self.current_target_size
        x = random.randint(size, SCREEN_WIDTH - size)
        y = random.randint(size, SCREEN_HEIGHT - size)
        self.targets.append(StaticTarget(x, y, size, DEFAULT_TARGET_LIFETIME))
