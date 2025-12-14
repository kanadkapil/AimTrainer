"""Weapon system for the FPS game."""


class Weapon:
    """Base weapon class with stats and behavior."""

    def __init__(
        self, name, damage, fire_rate, bullet_speed, spread, pellets=1, auto=False
    ):
        self.name = name
        self.damage = damage  # Damage per bullet
        self.fire_rate = fire_rate  # Shots per second
        self.bullet_speed = bullet_speed
        self.spread = spread  # Degrees of spread
        self.pellets = pellets  # Number of bullets per shot (for shotgun)
        self.auto = auto  # Full-auto or semi-auto
        self.cooldown = 1.0 / fire_rate  # Time between shots


# Define the three weapons
PISTOL = Weapon(
    name="Pistol",
    damage=25,
    fire_rate=3,  # 3 shots/sec
    bullet_speed=50,
    spread=0,  # Perfect accuracy
    pellets=1,
    auto=False,
)

AR_RIFLE = Weapon(
    name="AR Rifle",
    damage=15,
    fire_rate=8,  # 8 shots/sec
    bullet_speed=60,
    spread=2,  # Slight spread
    pellets=1,
    auto=True,
)

SHOTGUN = Weapon(
    name="Shotgun",
    damage=10,  # Per pellet
    fire_rate=1.5,  # 1.5 shots/sec
    bullet_speed=40,
    spread=15,  # Wide spread
    pellets=6,  # 6 pellets per shot
    auto=False,
)

# Weapon list for easy access
WEAPONS = [PISTOL, AR_RIFLE, SHOTGUN]
