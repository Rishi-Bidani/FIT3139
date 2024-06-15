import numpy as np
import matplotlib.pyplot as plt

# from tournament import SingleEliminationTournament
# from helper import get_stats
import tournament as t
import helper as h

states = ["Serve", "Return", "Rally", "Point Won by Server", "Point Won by Returner"]


def simulate_point(transition_matrix, initial_state=0):
    current_state = initial_state
    steps = 0
    while current_state < 3:
        current_state = np.random.choice(range(5), p=transition_matrix[current_state])
        steps += 1
    return current_state, steps


def simulate_game(player1, player2, transition_matrices, current_server=None):
    player1["score"] = 0
    player2["score"] = 0
    current_server = (
        np.random.choice([0, 1]) if current_server is None else current_server
    )
    while True:
        current_server = 1 - current_server
        winner, _ = simulate_point(transition_matrices[current_server])
        if current_server == 0:
            player1["score"] += 1 if winner == 3 else 0
            player2["score"] += 1 if winner == 4 else 0
        else:
            player1["score"] += 1 if winner == 4 else 0
            player2["score"] += 1 if winner == 3 else 0

        if player1["score"] >= 4 and player1["score"] >= player2["score"] + 2:
            break
        if player2["score"] >= 4 and player2["score"] >= player1["score"] + 2:
            break

    return player1["score"], player2["score"]


def simulate_set(player1, player2, transition_matrices):
    player1["games"] = 0
    player2["games"] = 0
    while True:
        score = simulate_game(player1, player2, transition_matrices)
        winner = 0 if score[0] > score[1] else 1
        player1["games"] += 1 if winner == 0 else 0
        player2["games"] += 1 if winner == 1 else 0

        # if 6 all, play tiebreak
        if player1["games"] == 6 and player2["games"] == 6:
            score = simulate_game(
                player1, player2, transition_matrices, current_server=winner
            )
            winner = 0 if score[0] > score[1] else 1
            player1["games"] += 1 if winner == 0 else 0
            player2["games"] += 1 if winner == 1 else 0
            break

        if player1["games"] >= 6 and player1["games"] >= player2["games"] + 2:
            break
        if player2["games"] >= 6 and player2["games"] >= player1["games"] + 2:
            break

    return player1["games"], player2["games"]


def simulate_match(player1, player2, transition_matrices, best_of=3):
    player1["sets"] = 0
    player2["sets"] = 0
    required_sets = (best_of + 1) // 2

    while True:
        score = simulate_set(player1, player2, transition_matrices)
        winner = 0 if score[0] > score[1] else 1
        player1["sets"] += 1 if winner == 0 else 0
        player2["sets"] += 1 if winner == 1 else 0

        if player1["sets"] >= required_sets:
            break
        if player2["sets"] >= required_sets:
            break

    return player1["sets"], player2["sets"]


def simulate_tournaments(players, best_of=3, num_tournaments=1000):
    for i, player in enumerate(players):
        player["name"] = f"Player {i + 1}"
    stats = {player["name"]: 0 for player in players}
    name_to_player = {player["name"]: player for player in players}

    all_results = []
    for _ in range(num_tournaments):
        tournament = t.SingleEliminationTournament(players, best_of=3)
        results = tournament.simulate()
        # for player in results:
        #     stats[player["name"]] += 1
        # winner = results[0]
        # stats[winner["name"]] += 1
        all_results.append(results)

    first_place = [result[0] for result in all_results]
    second_place = [result[1] for result in all_results]
    third_place = [result[2] for result in all_results]
    fourth_place = [result[3] for result in all_results]

    stats_first_place = h.get_stats(players, first_place)
    stats_second_place = h.get_stats(players, second_place)
    stats_third_place = h.get_stats(players, third_place)
    stats_fourth_place = h.get_stats(players, fourth_place)

    # histogram with 1st and 2nd place next to each other for each player

    fig, ax = plt.subplots()
    # increase figure size to show all player names
    fig.set_size_inches(10, 5)
    bar_width = 0.35
    index = np.arange(len(players))
    ax.bar(index, stats_first_place.values(), bar_width, label="1st Place")
    ax.bar(index + bar_width, stats_second_place.values(), bar_width, label="2nd Place")
    ax.set_xlabel("Players")
    ax.set_ylabel("Number of Wins")
    ax.set_title(f"Distribution of wins in {num_tournaments} tournaments")
    ax.set_xticks(index + bar_width / 2)
    ax.set_xticklabels(stats_first_place.keys())
    ax.legend()
    plt.show()
