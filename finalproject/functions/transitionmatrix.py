import numpy as np
from functions.helper import *


def create_transition_matrix(server_skill: int, returner_skill: int):
    # Ensure skills are between 0 and 1
    server_skill = np.clip(server_skill, 0, 1)
    returner_skill = np.clip(returner_skill, 0, 1)

    # Probabilities of success for each action
    p_return_success = returner_skill
    p_serve_win_direct = 1 - returner_skill
    p_serve_loss_direct = 1 - server_skill

    # Probabilities of failure for each action
    p_rally_continue = 1 - np.max([server_skill, returner_skill])
    p_server_win = 1 - returner_skill
    p_returner_win = 1 - server_skill
    p_rally_server_win = 1 - returner_skill
    p_rally_returner_win = 1 - server_skill

    # p_server_win, p_returner_win = proportional_scaling([server_skill, returner_skill], p_rally_continue)
    # p_rally_server_win, p_rally_returner_win = proportional_scaling([p_server_win, p_returner_win], p_rally_continue)

    # Transition matrix
    transition_matrix = np.array(
        [
            proportional_scaling(
                [0.0, p_return_success, 0.0, p_serve_win_direct, p_serve_loss_direct]
            ),  # Serve
            proportional_scaling(
                [0.0, 0.0, p_rally_continue, p_server_win, p_returner_win]
            ),  # Return
            proportional_scaling(
                [0.0, 0.0, p_rally_continue, p_rally_server_win, p_rally_returner_win]
            ),  # Rally
            [0.0, 0.0, 0.0, 1.0, 0.0],  # Point Won by Server (Terminal)
            [0.0, 0.0, 0.0, 0.0, 1.0],  # Point Won by Returner (Terminal)
        ]
    )

    return transition_matrix


def create_transition_matrices(player1: Player, player2: Player):
    # Transition matrix for player 1 serving
    transition_matrix_serve_p1 = create_transition_matrix(player1.Serve, player2.Return)
    # Transition matrix for player 2 serving
    transition_matrix_serve_p2 = create_transition_matrix(player2.Serve, player1.Return)
    return transition_matrix_serve_p1, transition_matrix_serve_p2
