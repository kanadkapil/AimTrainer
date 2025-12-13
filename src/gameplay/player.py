from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController


class FPSPlayer(FirstPersonController):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.cursor = None  # We'll use a custom crosshair later
        self.gun = Entity(
            parent=camera.ui,
            model="cube",
            color=color.blue,
            scale=(0.2, 0.2, 1),
            position=(0.5, -0.5),
            rotation=(-5, -5, 0),
        )
        self.max_lives = 3
        self.lives = 3

    def input(self, key):
        super().input(key)
        if key == "left mouse down":
            self.shoot()

    def shoot(self):
        # Visual feedback
        self.gun.position = (0.5, -0.4)
        self.gun.animate_position((0.5, -0.5), duration=0.1, curve=curve.linear)

        # Raycast
        hit_info = raycast(camera.world_position, camera.forward, distance=100)
        if hit_info.hit:
            if hasattr(hit_info.entity, "on_hit"):
                hit_info.entity.on_hit()
