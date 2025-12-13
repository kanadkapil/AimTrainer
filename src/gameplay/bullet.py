from ursina import *
import time


class Bullet(Entity):
    """Visible bullet projectile with physics and collision detection."""

    def __init__(
        self, position=(0, 0, 0), direction=(0, 0, 1), speed=50, owner=None, **kwargs
    ):
        super().__init__(
            model="sphere", scale=0.1, color=color.yellow, position=position, **kwargs
        )

        self.direction = Vec3(direction).normalized()
        self.speed = speed
        self.owner = owner  # Who fired this bullet (player or enemy)
        self.spawn_time = time.time()
        self.max_lifetime = 3.0  # seconds
        self.max_distance = 100  # units
        self.start_position = Vec3(position)

        # Visual trail effect
        self.trail = Entity(
            parent=self,
            model="cube",
            scale=(0.05, 0.05, 0.5),
            color=color.rgba(255, 255, 0, 100),
            rotation=(0, 0, 0),
            position=(0, 0, -0.25),
        )

    def update(self):
        # Move bullet
        self.position += self.direction * self.speed * time.dt

        # Check lifetime
        if time.time() - self.spawn_time > self.max_lifetime:
            destroy(self)
            return

        # Check max distance
        if distance(self.position, self.start_position) > self.max_distance:
            destroy(self)
            return

        # Collision detection
        hit_info = raycast(
            self.position - self.direction * 0.2,
            self.direction,
            distance=0.4,
            ignore=[self, self.owner],
        )

        if hit_info.hit:
            self.on_collision(hit_info.entity)
            destroy(self)

    def on_collision(self, hit_entity):
        """Called when bullet hits something."""
        # Check if hit a target
        if hasattr(hit_entity, "manager"):
            hit_entity.manager.on_target_hit(hit_entity)

        # Check if hit a player (for enemy bullets)
        if hasattr(hit_entity, "take_damage") and hit_entity != self.owner:
            hit_entity.take_damage(10)

        # Visual effect on hit (optional)
        # You can add particle effects here
