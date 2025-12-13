from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController
import time


class HealthPlayer(FirstPersonController):
    """FPS Player with health system for Survival Mode."""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.health = 100
        self.max_health = 100
        self.invulnerable_until = 0  # Timestamp for invulnerability frames
        self.invulnerable_duration = 1.0  # seconds

        # Health bar UI
        self.health_bar = Entity(
            parent=camera.ui,
            model="quad",
            scale=(0.3, 0.03),
            position=(-0.65, 0.40),
            color=color.red,
        )

        self.health_text = Text(
            text=f"HP: {self.health}/{self.max_health}",
            position=(-0.85, 0.38),
            scale=1.2,
            color=color.white,
        )

    def take_damage(self, amount):
        """Reduce health by amount if not invulnerable."""
        current_time = time.time()

        if current_time < self.invulnerable_until:
            return  # Still invulnerable

        self.health = max(0, self.health - amount)
        self.invulnerable_until = current_time + self.invulnerable_duration

        # Update UI
        health_ratio = self.health / self.max_health
        self.health_bar.scale_x = 0.3 * health_ratio
        self.health_text.text = f"HP: {self.health}/{self.max_health}"

        # Flash red on damage
        self.health_bar.color = color.rgba(255, 0, 0, 255)
        invoke(setattr, self.health_bar, "color", color.red, delay=0.2)

        # Check death
        if self.health <= 0:
            self.on_death()

    def on_death(self):
        """Called when health reaches 0."""
        # GameManager will handle this via checking player.health
        pass

    def heal(self, amount):
        """Restore health by amount."""
        self.health = min(self.max_health, self.health + amount)
        health_ratio = self.health / self.max_health
        self.health_bar.scale_x = 0.3 * health_ratio
        self.health_text.text = f"HP: {self.health}/{self.max_health}"
