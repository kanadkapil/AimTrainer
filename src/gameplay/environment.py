from ursina import *


class Arena(Entity):
    def __init__(self):
        super().__init__()
        # Floor
        Entity(
            model="plane",
            scale=(50, 1, 50),
            color=color.gray,
            texture="white_cube",
            texture_scale=(50, 50),
            collider="box",
        )

        # Walls
        wall_color = color.dark_gray
        Entity(
            model="cube",
            scale=(50, 10, 1),
            position=(0, 5, 25),
            color=wall_color,
            collider="box",
        )
        Entity(
            model="cube",
            scale=(50, 10, 1),
            position=(0, 5, -25),
            color=wall_color,
            collider="box",
        )
        Entity(
            model="cube",
            scale=(1, 10, 50),
            position=(25, 5, 0),
            color=wall_color,
            collider="box",
        )
        Entity(
            model="cube",
            scale=(1, 10, 50),
            position=(-25, 5, 0),
            color=wall_color,
            collider="box",
        )

        # Light
        PointLight(parent=camera, color=color.white, position=(0, 10, -10))
        AmbientLight(color=color.rgba(100, 100, 100, 0.1))
