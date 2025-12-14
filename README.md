# 🎯 FPS Aim Trainer & Survival

A high-performance 3D FPS game built with Python and Ursina Engine. Features two distinct game modes, a weapon class system, enemy AI, and procedural environments.

![Ursina Engine](https://img.shields.io/badge/Engine-Ursina-red) ![Python](https://img.shields.io/badge/Language-Python_3.13+-blue)

## ✨ Features

### 🎮 Game Modes

1.  **Practice Mode** 🎯

    - Focus on aim training with static and moving targets.
    - No enemies, no health loss—just pure shooting mechanics.
    - Score tracking for accuracy improvements.

2.  **Survival Mode** ☠️
    - Intense combat against tracking Enemy Turrets.
    - **Health System**: Player has 100 HP. Avoid enemy fire!
    - **Procedural Map**: Obstacles (walls, pillars, crates) are randomized every round.
    - Score points by destroying enemies and surviving.

### 🔫 Weapon System

Switch weapons on the fly to adapt to combat:

- **[1] Pistol**: Semi-auto sidearm. Accurate and reliable. (25 Dmg)
- **[2] AR Rifle**: Full-auto assault rifle. High rate of fire. (15 Dmg)
- **[3] Shotgun**: Burst-fire close quarters weapon. Fires 6 pellets. (10x6 Dmg)

### 🌍 Immersive Environment

- **Dynamic Visuals**: Blue skybox, directional sun, and soft shadows.
- **Procedural Nature**: Randomly generated trees and grass floor.
- **Physics**: Visible projectiles with accurate collision detection.

---

## 🚀 Installation

### Prerequisites

- Python 3.8 or newer (Approved for Python 3.13)
- Pip (Python Package Installer)

### Setup

1.  **Clone the repository** (or download source):

    ```bash
    git clone https://github.com/yourusername/fps-aim-trainer.git
    cd fps-aim-trainer
    ```

2.  **Install Dependencies**:
    ```bash
    pip install -r requirements.txt
    ```
    _(Note: Primarily requires `ursina`)_

---

## 🕹️ Controls

| Key                 | Action                                 |
| :------------------ | :------------------------------------- |
| **W, A, S, D**      | Move Player                            |
| **Mouse**           | Look Around                            |
| **Left Click**      | Shoot / Attack                         |
| **Hold Left Click** | Auto-Fire (AR Rifle)                   |
| **SPACE**           | Jump                                   |
| **1 / 2 / 3**       | Switch Weapons (Pistol / AR / Shotgun) |
| **ESC**             | Unlock Mouse / Quit Menu               |
| **R**               | Restart (Game Over Screen)             |

---

## 🛠️ Project Structure

- `main.py`: Entry point. Launches the Ursina application.
- `src/core/`: Application setup and settings.
  - `app_3d.py`: Core logic, Game Loop, and `GameManager`.
- `src/gameplay/`: Game entities and mechanics.
  - `player.py`: FPS Controller logic.
  - `weapons.py`: Weapon stats and definitions.
  - `enemy.py`: AI turret behavior.
  - `environment.py`: Arena generation (Map, Sky, Trees).
  - `bullet.py`: Projectile physics.

## 🤝 Credits

Built with [Ursina Engine](https://www.ursinaengine.org/).
Developed by [Your Name/User].
