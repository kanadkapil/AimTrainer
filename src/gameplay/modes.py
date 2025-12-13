import random
import pygame
from src.core.settings import *
from .targets import StaticTarget, MovingTarget
from src.data.logger import DataLogger
from src.ai.agent import AIAgent


class GameMode:
    def __init__(self, lives=3):
        self.targets = []
        self.score = 0
        self.lives = lives
        self.max_lives = lives
        self.last_spawn_time = 0
        self.game_over = False

        # AI & Data
        self.logger = DataLogger()
        self.agent = AIAgent()

        # Dynamic Parameters
        self.spawn_rate = TARGET_SPAWN_RATE
        self.current_target_size = DEFAULT_TARGET_SIZE

    def update(self):
        if self.lives <= 0:
            self.game_over = True
            return

        current_time = pygame.time.get_ticks()

        # Spawn new targets
        if current_time - self.last_spawn_time > self.spawn_rate:
            self.spawn_target()
            self.last_spawn_time = current_time

        # Update existing targets
        active_targets = []
        for t in self.targets:
            t.update()
            if t.active:
                active_targets.append(t)
            else:
                # Target expired naturally -> Lose a life
                self.lives -= 1
                self.logger.log_event("EXPIRED", t.x, t.y)

        self.targets = active_targets

    def draw(self, surface):
        for target in self.targets:
            target.draw(surface)

    def handle_click(self, pos):
        if self.game_over:
            return False

        hit = False
        click_time = pygame.time.get_ticks()

        for target in self.targets:
            if target.check_collision(pos[0], pos[1]):
                target.active = False  # Remove target
                self.score += 1
                hit = True

                # Calculate reaction time
                reaction_time = click_time - target.spawn_time
                self.logger.log_event("HIT", pos[0], pos[1], f"time={reaction_time}ms")

                # AI Analysis
                new_params = self.agent.analyze_performance(True, reaction_time)
                self.apply_params(new_params)
                break

        if not hit:
            self.lives -= 1
            self.logger.log_event("MISS", pos[0], pos[1])
            new_params = self.agent.analyze_performance(False, 0)
            self.apply_params(new_params)

        return hit

    def apply_params(self, params):
        if "spawn_rate" in params:
            self.spawn_rate = params["spawn_rate"]
        if "target_size" in params:
            self.current_target_size = params["target_size"]

    def spawn_target(self):
        pass


class FlickMode(GameMode):
    def spawn_target(self):
        size = self.current_target_size
        x = random.randint(size, SCREEN_WIDTH - size)
        y = random.randint(size, SCREEN_HEIGHT - size)
        self.targets.append(StaticTarget(x, y, size, DEFAULT_TARGET_LIFETIME))


class SurvivalMode(GameMode):
    def __init__(self):
        super().__init__(lives=5)

    def spawn_target(self):
        size = self.current_target_size
        x = random.randint(size, SCREEN_WIDTH - size)
        y = random.randint(size, SCREEN_HEIGHT - size)

        # 30% chance of Moving Target
        if random.random() < 0.3:
            speed = 2 + (self.score * 0.05)  # Speed increases with score
            self.targets.append(
                MovingTarget(x, y, size, DEFAULT_TARGET_LIFETIME, speed=speed)
            )
        else:
            self.targets.append(StaticTarget(x, y, size, DEFAULT_TARGET_LIFETIME))
