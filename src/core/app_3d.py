from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController
import random
import time
from src.core.settings import *
from src.gameplay.player import FPSPlayer
from src.gameplay.environment import Arena
from src.gameplay.targets_3d import Target3D, MovingTarget3D


class GameManager(Entity):
    def __init__(self):
        super().__init__()
        self.state = "MENU"  # MENU, PLAYING, GAMEOVER
        self.score = 0
        self.last_spawn = 0
        self.spawn_rate = 1.0

        # UI
        self.menu_text = Text(
            text="Press 'P' to Play", origin=(0, 0), scale=2, color=color.white
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
            # Reset lives if possible
            if hasattr(self.player, "lives"):
                self.player.lives = 3

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

            self.score_text.text = f"Score: {self.score}"

            # Game Over Logic - lives check (assuming player doesn't decrement lives yet, but sticking to placeholder)
            # Realistically we need a way to track lives. For now, let's just rely on manual game over or add lives logic here.
            pass

    def spawn_target(self):
        x = random.uniform(-20, 20)
        y = random.uniform(1, 8)
        z = random.uniform(0, 20)
        t = Target3D(position=(x, y, z))
        t.manager = self

    def on_target_hit(self, target):
        self.score += 1

    def shoot(self):
        if self.gun and not self.gun.on_cooldown:
            self.gun.on_cooldown = True
            self.gun.animate_position((0.5, -0.4), duration=0.1, curve=curve.linear)
            invoke(
                lambda: self.gun.animate_position((0.5, -0.5), duration=0.1), delay=0.1
            )
            invoke(setattr, self.gun, "on_cooldown", False, delay=0.2)

            hit_info = raycast(camera.world_position, camera.forward, distance=100)
            if hit_info.hit:
                if hasattr(hit_info.entity, "manager"):
                    hit_info.entity.manager.on_target_hit(hit_info.entity)
                    destroy(hit_info.entity)

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
        if key == "p" and self.state == "MENU":
            self.start_game()
        if key == "r" and self.state == "GAMEOVER":
            self.menu_text.text = "Press 'P' to Play"
            self.state = "MENU"


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

        # Player
        self.gm.player = FirstPersonController(position=(0, 2, -15))
        self.gm.player.enabled = False

    def run(self):
        self.app.run()
