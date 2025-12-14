from ursina import *
import random


class Arena(Entity):
    def __init__(self):
        super().__init__()
        # Environment Atmosphere
        self.sky = Sky(texture="sky_default")
        # Sun
        self.sun = DirectionalLight(shadows=True)
        self.sun.look_at(Vec3(1, -1, 1))

        # Ground Texturing (simulate grass color)
        # Using a greener color for grass
        grass_color = color.rgb(50, 150, 50)

        # Create base floor
        self.floor = Entity(
            model="plane",
            scale=(100, 1, 100),
            color=grass_color,
            texture="grass",  # Ursina has a default grass texture usually, or white_cube tinted
            texture_scale=(50, 50),
            collider="box",
        )

        # Nature Elements (Trees)
        self.add_trees()

        # Randomized Layout
        self.add_random_obstacles()

    def add_trees(self):
        """Add procedural trees around the arena border."""
        for i in range(20):
            # Random position on outer rim
            x = random.choice([random.uniform(-40, -20), random.uniform(20, 40)])
            z = random.uniform(-40, 40)
            if random.random() > 0.5:  # Swap axes sometimes
                x, z = z, x

            # Tree Trunk
            trunk = Entity(
                model="cylinder",
                scale=(1, 4, 1),
                position=(x, 2, z),
                color=color.rgb(100, 50, 0),
                collider="box",
            )
            # Tree Leaves
            leaves = Entity(
                model="cone",  # Low poly style
                scale=(3, 4, 3),
                position=(x, 5, z),
                color=color.rgb(20, 100, 20),
                collider="box",
            )

    def add_random_obstacles(self):
        """Generate a random maze/cover layout."""
        # Clear previous obstacles if any (not tracking them currently but for restart logic it's good practice)
        # For now just spawn new ones

        num_obstacles = 12
        for _ in range(num_obstacles):
            # Try to find a spot not too close to center (0,0) where player spawns
            while True:
                x = random.randint(-20, 20)
                z = random.randint(-20, 20)
                if abs(x) > 5 or abs(z) > 5:  # Keep center clear
                    break

            # Randomize type
            if random.random() < 0.3:
                # Tall Pillar
                Entity(
                    model="cube",
                    scale=(2, 6, 2),
                    position=(x, 3, z),
                    color=color.gray,
                    texture="brick",
                    collider="box",
                )
            elif random.random() < 0.6:
                # Wide Wall
                is_horizontal = random.random() > 0.5
                scale = (6, 3, 1) if is_horizontal else (1, 3, 6)
                Entity(
                    model="cube",
                    scale=scale,
                    position=(x, 1.5, z),
                    color=color.dark_gray,
                    collider="box",
                )
            else:
                # Crate
                Entity(
                    model="cube",
                    scale=(1.5, 1.5, 1.5),
                    position=(x, 0.75, z),
                    color=color.orange,
                    texture="crate",  # Ursina default sometimes
                    collider="box",
                )
