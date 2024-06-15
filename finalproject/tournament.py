import simulation as simulation
import transitionmatrix as markov
import helper as h


class SingleEliminationTournament:
    def __init__(self, players, best_of=3):
        self.players = players
        self.best_of = best_of
        self.results = None

    def simulate_round(self, player1, player2):
        transition_matrices = markov.create_transition_matrices(player1, player2)
        winner = simulation.simulate_match(
            player1, player2, transition_matrices, best_of=self.best_of
        )
        return player1 if winner[0] > winner[1] else player2

    def simulate(self) -> list[h.Player]:
        """Simulates the tournament and returns the top 4 players.
        This is a simple single elimination tournament and only works with more than 4 players.
        I did not do error checking and handling of edge cases to keep the code and within the scope of the assignment.

        Returns:
            list[Player]: The top 4 players in the tournament
        """
        # make groups of 2
        brackets = [self.players[i : i + 2] for i in range(0, len(self.players), 2)]
        while len(brackets) > 2:
            # there are more than 4 players remaining
            # simulate each bracket
            winners = []
            for bracket in brackets:
                winner = self.simulate_round(bracket[0], bracket[1])
                winners.append(winner)
            brackets = [winners[i : i + 2] for i in range(0, len(winners), 2)]

        # there are 2 brackets remaining
        # simulate both of them and return the ranking of the players
        self.results = []
        final_winners = []
        final_loosers = []
        for bracket in brackets:
            winner = self.simulate_round(bracket[0], bracket[1])
            final_winners.append(winner)
            final_loosers.append(bracket[0] if winner == bracket[1] else bracket[1])
        # simulate the final match
        final_winner = self.simulate_round(final_winners[0], final_winners[1])
        final_looser = (
            final_loosers[0] if final_winner == final_winners[1] else final_loosers[1]
        )
        self.results = [final_winner, final_looser]
        # simulate the 3rd place match
        third_place = self.simulate_round(final_loosers[0], final_loosers[1])
        fourth_place = (
            final_loosers[0] if third_place == final_loosers[1] else final_loosers[1]
        )
        self.results.append(third_place)
        self.results.append(fourth_place)

        return self.results
