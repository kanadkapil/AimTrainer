import random
from src.core.settings import *


class AIAgent:
    def __init__(self):
        self.performance_history = []  # List of hits/misses or reaction times
        self.current_difficulty = 1.0  # Multiplier

    def analyze_performance(self, hit, reaction_time):
        """Called after every shot"""
        self.performance_history.append({"hit": hit, "time": reaction_time})
        if len(self.performance_history) > 10:
            self.performance_history.pop(0)

        return self.adapt_difficulty()

    def adapt_difficulty(self):
        """Simplistic heuristic for now: Adjust difficulty based on recent accuracy"""
        if not self.performance_history:
            return {}

        hits = sum(1 for p in self.performance_history if p["hit"])
        accuracy = hits / len(self.performance_history)

        # Difficulty parameters
        new_params = {}

        if accuracy > 0.8:
            # Increase difficulty
            self.current_difficulty += 0.05
            new_params["spawn_rate"] = max(
                200, int(TARGET_SPAWN_RATE / self.current_difficulty)
            )
            new_params["target_size"] = max(
                10, int(DEFAULT_TARGET_SIZE / self.current_difficulty)
            )
        elif accuracy < 0.4:
            # Decrease difficulty
            self.current_difficulty = max(0.5, self.current_difficulty - 0.05)
            new_params["spawn_rate"] = max(
                200, int(TARGET_SPAWN_RATE / self.current_difficulty)
            )
            new_params["target_size"] = max(
                10, int(DEFAULT_TARGET_SIZE / self.current_difficulty)
            )

        print(f"AI Adaptation: Acc={accuracy:.2f}, Diff={self.current_difficulty:.2f}")
        return new_params
