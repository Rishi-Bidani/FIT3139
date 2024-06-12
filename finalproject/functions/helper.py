from dataclasses import dataclass
import numpy as np


def proportional_scaling(arr, max_val=1.0):
    arr = np.array(arr)
    total = np.sum(arr)
    if total == 0:
        return arr
    # return [max_val * x / total for x in arr]
    return max_val * arr / total


def get_stats(players, results):
    stats = {player["name"]: 0 for player in players}
    for player in results:
        stats[player["name"]] += 1
    return stats


@dataclass
class Player:
    Serve: float
    Return: float
    name: str = ""
    sets: int = 0
    games: int = 0
    score: int = 0
    wins: int = 0

    def __setitem__(self, key, value):
        setattr(self, key, value)

    def __getitem__(self, item):
        return getattr(self, item)

    def __str__(self):
        return self.name
