from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController
import random
import time
from src.core.settings import *
from src.gameplay.player import FPSPlayer
from src.gameplay.health_player import HealthPlayer
from src.gameplay.enemy import Enemy
from src.gameplay.environment import Arena
from src.gameplay.targets_3d import Target3D, MovingTarget3D


class GameManager(Entity):
    def __init__(self):
        super().__init__()
        self.state = "MENU"  # MENU, PLAYING, GAMEOVER
        self.game_mode = None  # "practice" or "survival"
        self.score = 0
        self.last_spawn = 0
        self.spawn_rate = 1.0
        self.enemies = []  # Track spawned enemies
        self.enemy_spawn_interval = 5.0  # Spawn enemy every 5 seconds (Survival only)
        self.last_enemy_spawn = 0

        # UI
        self.menu_text = Text(
            text="Choose Mode:\n1 - Practice Mode\n2 - Survival Mode",
            origin=(0, 0),
            scale=1.5,
            color=color.white,
        )
        self.score_text = Text(
            text="", position=(-0.85, 0.45), scale=1.5, enabled=False
        )

        # References
        self.player = None
        self.arena = None
        self.gun = None

    def start_game(self):
        self.state = "PLAYING"
        self.menu_text.enabled = False

        if self.player:
            self.player.enabled = True
            self.player.position = (0, 2, -15)
            # Reset health for survival mode
            if hasattr(self.player, "health"):
                if self.game_mode == "survival":
                    self.player.health = 100
                    self.player.max_health = 100

        self.score = 0
        self.score_text.enabled = True
        mouse.locked = True

        # Initialize gun if needed
        if not self.gun:
            self.gun = Entity(
                parent=camera.ui,
                model="cube",
                scale=(0.5, 0.3, 1),
                position=(0.5, -0.5),
                color=color.dark_gray,
                on_cooldown=False,
                rotation=(-5, -5, 0),
            )

    def update(self):
        if self.state == "PLAYING":
            # Spawning Logic
            if time.time() - self.last_spawn > self.spawn_rate:
                self.spawn_target()
                self.last_spawn = time.time()

            # Enemy spawning (Survival mode only)
            if self.game_mode == "survival":
                if time.time() - self.last_enemy_spawn > self.enemy_spawn_interval:
                    self.spawn_enemy()
                    self.last_enemy_spawn = time.time()

            mode_name = "Practice" if self.game_mode == "practice" else "Survival"
            self.score_text.text = f"Mode: {mode_name} | Score: {self.score}"

            # Game Over check for Survival mode
            if self.game_mode == "survival" and hasattr(self.player, "health"):
                if self.player.health <= 0:
                    self.game_over()

    def spawn_target(self):
        x = random.uniform(-20, 20)
        y = random.uniform(1, 8)
        z = random.uniform(0, 20)

        if random.random() < 0.5:  # 50% chance of moving target
            t = MovingTarget3D(position=(x, y, z), speed=random.uniform(2, 5))
        else:
            t = Target3D(position=(x, y, z))

        t.manager = self

    def on_target_hit(self, target):
        self.score += 1

    def spawn_enemy(self):
        """Spawn an enemy turret at a random position."""
        # Spawn away from player
        x = random.choice([-15, -10, 10, 15])
        z = random.choice([5, 10, 15])

        enemy = Enemy(position=(x, 1, z))
        enemy.player_ref = self.player
        enemy.game_manager = self
        self.enemies.append(enemy)

    def on_enemy_killed(self, enemy):
        """Called when an enemy is destroyed."""
        if enemy in self.enemies:
            self.enemies.remove(enemy)
        self.score += 5  # Bonus points for killing enemies

    def shoot(self):
        if self.gun and not self.gun.on_cooldown:
            self.gun.on_cooldown = True
            self.gun.animate_position((0.5, -0.4), duration=0.1, curve=curve.linear)
            invoke(
                lambda: self.gun.animate_position((0.5, -0.5), duration=0.1), delay=0.1
            )
            invoke(setattr, self.gun, "on_cooldown", False, delay=0.2)

            # Spawn visible bullet
            from src.gameplay.bullet import Bullet

            bullet = Bullet(
                position=camera.world_position + camera.forward * 0.5,
                direction=camera.forward,
                speed=50,
                owner=self.player,
            )

    def game_over(self):
        self.state = "GAMEOVER"
        if self.player:
            self.player.enabled = False
        mouse.locked = False
        self.menu_text.text = f"GAME OVER\nScore: {self.score}\nPress 'R' to Restart"
        self.menu_text.enabled = True

    def input(self, key):
        if key == "left mouse down" and self.state == "PLAYING":
            self.shoot()

        if key == "escape":
            mouse.locked = False
            application.quit()

        # Mode selection
        if self.state == "MENU":
            if key == "1":
                self.game_mode = "practice"
                self.start_game()
            elif key == "2":
                self.game_mode = "survival"
                self.start_game()

        # Restart
        if key == "r" and self.state == "GAMEOVER":
            self.menu_text.text = "Choose Mode:\n1 - Practice Mode\n2 - Survival Mode"
            self.state = "MENU"
            self.game_mode = None


class AimTrainer3D:
    def __init__(self):
        self.app = Ursina()

        # Window Settings (Defaults)
        window.title = "Aim Trainer 3D"

        self.setup_scene()

    def setup_scene(self):
        # Game Manager
        self.gm = GameManager()

        # Environment
        self.gm.arena = Arena()

        # Player - use different controller based on mode
        # For now, always use HealthPlayer (works for both modes)
        self.gm.player = HealthPlayer(position=(0, 2, -15))
        self.gm.player.enabled = False

    def run(self):
        self.app.run()
