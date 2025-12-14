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
from src.gameplay.bullet import Bullet
from src.gameplay.weapons import WEAPONS, PISTOL, AR_RIFLE, SHOTGUN


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

        # Weapon System
        self.current_weapon = PISTOL  # Start with pistol
        self.last_shot_time = 0
        self.mouse_held = False  # For auto-fire

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
        self.weapon_text = Text(
            text="", position=(-0.85, 0.4), scale=1, enabled=False, color=color.yellow
        )

        # References
        self.player = None
        self.arena = None
        self.gun = None

    def start_game(self, mode):
        self.state = "PLAYING"
        self.game_mode = mode
        self.score = 0
        self.last_spawn = time.time()
        self.last_enemy_spawn = time.time()
        self.current_weapon = PISTOL  # Reset to pistol

        mouse.locked = True
        self.menu_text.enabled = False
        self.score_text.enabled = True
        self.weapon_text.enabled = True  # Show weapon UI

        if self.player:
            self.player.enabled = True
            self.player.position = (0, 2, -15)
            # Reset health for survival mode
            if hasattr(self.player, "health"):
                if self.game_mode == "survival":
                    self.player.health = 100
                    self.player.max_health = 100

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
            # Auto-fire for auto weapons
            if self.mouse_held and self.current_weapon.auto:
                if time.time() - self.last_shot_time >= self.current_weapon.cooldown:
                    self.shoot()

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
            self.weapon_text.text = f"Weapon: {self.current_weapon.name} [1/2/3]"

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

    def switch_weapon(self, weapon_index):
        """Switch to a different weapon."""
        self.current_weapon = WEAPONS[weapon_index]
        self.last_shot_time = 0  # Reset cooldown
        print(f"Switched to {self.current_weapon.name}")

    def shoot(self):
        """Fire the current weapon."""
        current_time = time.time()

        # Check cooldown
        if current_time - self.last_shot_time < self.current_weapon.cooldown:
            return

        self.last_shot_time = current_time

        # Gun recoil animation
        if self.gun:
            self.gun.on_cooldown = True
            self.gun.position = (
                camera.position + camera.forward * 1.5 + camera.down * 0.3
            )
            self.gun.animate_position(
                camera.position + camera.forward * 2 + camera.down * 0.5,
                duration=0.05,
                curve=curve.out_bounce,
            )
            invoke(
                setattr,
                self.gun,
                "on_cooldown",
                False,
                delay=self.current_weapon.cooldown,
            )

            # Return gun to idle position
            invoke(
                self.gun.animate_position,
                camera.position + camera.forward * 2 + camera.down * 0.5,
                delay=self.current_weapon.cooldown * 0.5,
            )

        # Spawn bullets based on weapon
        for i in range(self.current_weapon.pellets):
            # Calculate spread
            spread_x = random.uniform(
                -self.current_weapon.spread, self.current_weapon.spread
            )
            spread_y = random.uniform(
                -self.current_weapon.spread, self.current_weapon.spread
            )

            # Direction with spread
            base_direction = camera.forward
            spread_direction = (
                base_direction
                + camera.right * spread_x * 0.01
                + camera.up * spread_y * 0.01
            )
            spread_direction = spread_direction.normalized()

            # Spawn from gun tip if gun exists, otherwise from camera
            if self.gun:
                spawn_pos = camera.world_position + camera.forward * 2 + camera.up * 0.5
            else:
                spawn_pos = camera.world_position + camera.forward * 1

            bullet = Bullet(
                position=spawn_pos,
                direction=spread_direction,
                speed=self.current_weapon.bullet_speed,
                owner=self.player,
            )
            bullet.damage = self.current_weapon.damage  # Set bullet damage

    def game_over(self):
        self.state = "GAMEOVER"
        if self.player:
            self.player.enabled = False
        mouse.locked = False
        self.menu_text.text = f"GAME OVER\nScore: {self.score}\nPress 'R' to Restart"
        self.menu_text.enabled = True
        self.weapon_text.enabled = False

    def input(self, key):
        if key == "escape":
            mouse.locked = False
            application.quit()

        # Menu state
        if self.state == "MENU":
            if key == "1":
                self.start_game("practice")
            elif key == "2":
                self.start_game("survival")

        # Playing state
        elif self.state == "PLAYING":
            # Weapon switching
            if key == "1":
                self.switch_weapon(0)  # Pistol
            elif key == "2":
                self.switch_weapon(1)  # AR Rifle
            elif key == "3":
                self.switch_weapon(2)  # Shotgun

            # Shooting
            if key == "left mouse down":
                self.mouse_held = True
                self.shoot()
            elif key == "left mouse up":
                self.mouse_held = False

        # Game over state
        elif self.state == "GAMEOVER":
            if key == "r":
                self.menu_text.text = (
                    "Choose Mode:\n1 - Practice Mode\n2 - Survival Mode"
                )
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
