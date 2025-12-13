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

        # Add cover obstacles
        self.add_obstacles()

    def add_obstacles(self):
        """Add walls and crates for tactical cover."""
        # Interior walls for cover
        cover_walls = [
            (-10, 1.5, 5, 2, 3, 0.5),  # x, y, z, sx, sy, sz
            (10, 1.5, 5, 2, 3, 0.5),
            (0, 1.5, 15, 4, 3, 0.5),
            (-5, 1.5, -5, 0.5, 3, 2),
            (5, 1.5, -5, 0.5, 3, 2),
        ]

        for x, y, z, sx, sy, sz in cover_walls:
            Entity(
                model="cube",
                scale=(sx, sy, sz),
                position=(x, y, z),
                color=color.rgba(80, 80, 80),
                collider="box",
            )
