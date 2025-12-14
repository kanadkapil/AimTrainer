from ursina import *
import random
import time


class Enemy(Entity):
    """Enemy turret that tracks and shoots at the player."""

    def __init__(self, position=(0, 0, 0), **kwargs):
        super().__init__(
            model="cube",
            color=color.rgb(150, 50, 50),  # Dark red
            scale=(1, 1.5, 1),
            position=position,
            collider="box",
            **kwargs,
        )

        # Enemy stats
        self.health = 50
        self.max_health = 50
        self.damage = 10
        self.shoot_cooldown = 2.0  # Seconds between shots
        self.last_shot_time = 0
        self.shoot_range = 40  # Range to shoot player
        self.accuracy = 0.8  # 80% accuracy (adds random offset)

        # Visual indicator (gun barrel)
        self.barrel = Entity(
            parent=self,
            model="cube",
            scale=(0.2, 0.2, 1),
            position=(0, 0.3, 0.6),
            color=color.dark_gray,
        )

        # Health bar above enemy
        self.health_bar_bg = Entity(
            parent=self,
            model="quad",
            scale=(1, 0.1),
            position=(0, 1.2, 0),
            color=color.black,
            billboard=True,
        )

        self.health_bar = Entity(
            parent=self.health_bar_bg,
            model="quad",
            scale=(1, 1),
            position=(0, 0, -0.01),
            color=color.red,
            origin=(-0.5, 0),
        )

        self.player_ref = None
        self.game_manager = None

    def update(self):
        if not self.player_ref or not self.game_manager:
            return

        # Look at player
        self.look_at(self.player_ref)

        # Shoot if player in range
        distance_to_player = distance(self.position, self.player_ref.position)
        current_time = time.time()

        if distance_to_player < self.shoot_range:
            if current_time - self.last_shot_time > self.shoot_cooldown:
                self.shoot_at_player()
                self.last_shot_time = current_time

    def shoot_at_player(self):
        """Fire a bullet towards the player."""
        if not self.player_ref:
            return

        # Calculate direction to player with accuracy offset
        direction = (self.player_ref.position - self.position).normalized()

        # Add inaccuracy
        if random.random() > self.accuracy:
            offset = Vec3(
                random.uniform(-0.3, 0.3),
                random.uniform(-0.3, 0.3),
                random.uniform(-0.3, 0.3),
            )
            direction = (direction + offset).normalized()

        # Spawn bullet
        from src.gameplay.bullet import Bullet

        bullet = Bullet(
            position=self.position + Vec3(0, 0.5, 0),
            direction=direction,
            speed=30,
            owner=self,
        )
        bullet.color = color.orange  # Enemy bullets are orange

    def take_damage(self, amount):
        """Reduce enemy health."""
        self.health = max(0, self.health - amount)

        # Update health bar
        health_ratio = self.health / self.max_health
        self.health_bar.scale_x = health_ratio

        # Flash white on damage
        original_color = self.color
        self.color = color.white
        invoke(setattr, self, "color", original_color, delay=0.1)

        # Destroy if dead
        if self.health <= 0:
            self.on_death()

    def on_death(self):
        """Called when enemy is destroyed."""
        if self.game_manager:
            self.game_manager.on_enemy_killed(self)
        destroy(self)
