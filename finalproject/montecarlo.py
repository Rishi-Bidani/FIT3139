import matplotlib.pyplot as plt

# from helper import *
# from simulation import *
# from transitionmatrix import *
import helper as h
import simulation as simulation
import transitionmatrix as markov


# simulate a point many times
def _monte_carlo_point(player1, player2, reps=1000):
    winner_player1_serving = {"player1": 0, "player2": 0}
    winner_player2_serving = {"player1": 0, "player2": 0}
    transition_matrices = markov.create_transition_matrices(player1, player2)

    for _ in range(reps):
        winner1, _ = simulation.simulate_point(transition_matrices[0])
        winner2, _ = simulation.simulate_point(transition_matrices[1])

        # winner 1 is when player 1 serves
        winner_player1_serving["player1"] += 1 if winner1 == 3 else 0
        winner_player1_serving["player2"] += 1 if winner1 == 4 else 0

        # winner 2 is when player 2 serves
        winner_player2_serving["player1"] += 1 if winner2 == 4 else 0
        winner_player2_serving["player2"] += 1 if winner2 == 3 else 0
    return "point", winner_player1_serving, winner_player2_serving


# simulate a set many times
def _monte_carlo_game(player1, player2, reps=1000):
    winner_player1 = {"player1": 0, "player2": 0}
    winner_player2 = {"player1": 0, "player2": 0}
    transition_matrices = markov.create_transition_matrices(player1, player2)
    for _ in range(reps):
        winner1 = simulation.simulate_game(player1, player2, transition_matrices)
        winner2 = simulation.simulate_game(player2, player1, transition_matrices)

        winner_player1["player1"] += 1 if winner1[0] > winner1[1] else 0
        winner_player1["player2"] += 1 if winner1[0] < winner1[1] else 0

        winner_player2["player2"] += 1 if winner2[0] > winner2[1] else 0
        winner_player2["player1"] += 1 if winner2[0] < winner2[1] else 0

    return "game", winner_player1, winner_player2


# simulate a game many times
def _monte_carlo_set(player1, player2, reps=1000):
    winners = {"player1": 0, "player2": 0}
    transition_matrices = markov.create_transition_matrices(player1, player2)

    for _ in range(reps):
        winner = simulation.simulate_set(player1, player2, transition_matrices)
        winners["player1"] += 1 if winner[0] > winner[1] else 0
        winners["player2"] += 1 if winner[0] < winner[1] else 0

    return "set", winners


# simulate a match many times
def _monte_carlo_match(player1, player2, reps=1000, best_of=3):
    winners = {"player1": 0, "player2": 0}
    transition_matrices = markov.create_transition_matrices(player1, player2)

    for _ in range(reps):
        winner = simulation.simulate_match(
            player1, player2, transition_matrices, best_of=best_of
        )
        winners["player1"] += 1 if winner[0] > winner[1] else 0
        winners["player2"] += 1 if winner[0] < winner[1] else 0

    return "match", winners


def plot_monte_carlo_simulation(
    player1: h.Player, player2: h.Player, function, reps=1000
) -> None:
    winners = function(player1, player2, reps)

    if len(winners) == 3:
        text, winner_player1_serving, winner_player2_serving = winners
        fig, ax = plt.subplots(1, 2, figsize=(10, 5))
        fig.suptitle(f"Monte Carlo Simulation of a {text}")
        ax[0].bar(winner_player1_serving.keys(), winner_player1_serving.values())
        ax[0].bar_label(ax[0].containers[0])
        ax[0].set_title("Player 1 Serving")
        ax[0].set_xlabel("Winner")
        ax[0].set_ylabel("Frequency")

        ax[1].bar(winner_player2_serving.keys(), winner_player2_serving.values())
        ax[1].bar_label(ax[1].containers[0])
        ax[1].set_title("Player 2 Serving")
        ax[1].set_xlabel("Winner")
        ax[1].set_ylabel("Frequency")
        plt.show()

    elif len(winners) == 2:
        text, winners = winners
        fig, ax = plt.subplots()
        ax.set_title(f"Monte Carlo Simulation of a {text}")
        ax.bar(winners.keys(), winners.values())
        ax.bar_label(ax.containers[0])
        ax.set_xlabel("Winner")
        ax.set_ylabel("Frequency")
        plt.show()
