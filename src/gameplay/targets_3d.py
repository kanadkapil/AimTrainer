from ursina import *
import random


class Target3D(Entity):
    def __init__(self, position=(0, 0, 0), scale=1, lifetime=3.0):
        super().__init__(
            model="sphere",
            color=color.red,
            scale=scale,
            position=position,
            collider="sphere",
        )
        self.lifetime = lifetime
        self.spawn_time = time.time()

        # Random shape/color
        shapes = ["sphere", "cube"]
        self.model = random.choice(shapes)
        if self.model.name == "cube":
            self.collider = "box"

        self.color = random.choice([color.red, color.blue, color.green, color.yellow])

    def update(self):
        if time.time() - self.spawn_time > self.lifetime:
            # Expiration logic handled by manager usually, but we can self-destruct
            if hasattr(self, "on_expire"):
                self.on_expire()
            destroy(self)

    def on_hit(self):
        # Particle effect
        destroy(self)
        if hasattr(self, "manager"):
            self.manager.on_target_hit(self)


class MovingTarget3D(Target3D):
    def __init__(self, position=(0, 0, 0), scale=1, lifetime=3.0, speed=2):
        super().__init__(position, scale, lifetime)
        self.speed = speed
        self.direction = Vec3(
            random.uniform(-1, 1), random.uniform(-0.5, 0.5), 0
        ).normalized()

    def update(self):
        super().update()
        self.position += self.direction * self.speed * time.dt

        # Quick bounds check/bounce
        if abs(self.x) > 20:
            self.direction.x *= -1
        if abs(self.y) > 10 or self.y < 1:
            self.direction.y *= -1
