import itertools
import random
import copy
import matplotlib.pyplot as plt
import numpy as np
import scipy.signal


class Schelling:
    def __init__(self, width, height, empty_ratio, similarity_threshold, n_iterations, types=2):
        self.width = width
        self.height = height

        self.types = types
        self.empty_ratio = empty_ratio
        self.similarity_threshold = similarity_threshold
        self.n_iterations = n_iterations
        
        self.empty_houses = []
        self.agents = {}
        self.all_houses = list(itertools.product(range(self.width), range(self.height)))
        random.shuffle(self.all_houses)
        
        self.n_empty = int(self.empty_ratio * len(self.all_houses))
        self.empty_houses = self.all_houses[:self.n_empty]
        self.remaining_houses = self.all_houses[self.n_empty:]
        houses_by_type = [self.remaining_houses[i::self.types]for i in range(self.types)]
        
        for i in range(self.types):
                dictionary2 = dict(zip(houses_by_type[i], [i + 1] * len(houses_by_type[i])))
                d = self.agents.copy()
                d.update(dictionary2)
                self.agents = d

    def is_unsatisfied(self, x, y):
            type_ = self.agents[(x, y)]
            count_similar = 0
            count_different = 0
            if x > 0 and y > 0 and(x - 1, y - 1) not in self.empty_houses:
                if self.agents[(x - 1, y - 1)] == type_:
                    count_similar += 1
                else:
                    count_different += 1
            if y > 0 and (x, y - 1) not in self.empty_houses:
                if self.agents[(x, y - 1)] == type_:
                    count_similar += 1
                else:
                    count_different += 1
            if x < (self.width - 1) and y > 0 and (x + 1, y - 1) not in self.empty_houses:
                if self.agents[(x + 1, y - 1)] == type_:
                    count_similar += 1
                else:
                    count_different += 1
            if x > 0 and (x - 1, y) not in self.empty_houses:
                if self.agents[(x - 1, y)] == type_:
                    count_similar += 1
                else:
                    count_different += 1
            if x < (self.width - 1) and (x + 1, y) not in self.empty_houses:
                if self.agents[(x + 1, y)] == type_:
                    count_similar += 1
                else:
                    count_different += 1
            if x > 0 and y < (self.height - 1) and (x - 1, y + 1) not in self.empty_houses:
                if self.agents[(x - 1, y + 1)] == type_:
                    count_similar += 1
                else:
                    count_different += 1
            if x > 0 and y < (self.height - 1) and(x, y + 1) not in self.empty_houses:
                if self.agents[(x, y + 1)] == type_:
                    count_similar += 1
                else:
                    count_different += 1
            if x < (self.width - 1) and y < (self.height - 1) and (x + 1, y + 1) not in self.empty_houses:
                if self.agents[(x + 1, y + 1)] == type_:
                    count_similar += 1
                else:
                    count_different += 1
            if(count_similar + count_different) == 0:
                return False
            else:
                return float(count_similar) / (count_similar + count_different) < self.similarity_threshold

    def go(self):
        graph = []
        for i in range(self.n_iterations):
                self.old_agents = copy.deepcopy(self.agents)
                n_changes = 0
                for agent in self.old_agents:
                    if self.is_unsatisfied(agent[0], agent[1]):
                        agent_type = self.agents[agent]
                        empty_house = random.choice(self.empty_houses)
                        self.agents[empty_house] = agent_type
                        del self.agents[agent]
                        self.empty_houses.remove(empty_house)
                        self.empty_houses.append(agent)
                        n_changes += 1
                graph.append(n_changes)
                if n_changes == 0:
                    break
        return graph

    def move_to_empty(self, x, y):
            type_ = self.agents[(x, y)]
            empty_house = random.choice(self.empty_houses)
            self.updated_agents[empty_house] = type_
            del self.updated_agents[(x, y)]
            self.empty_houses.remove(empty_house)
            self.empty_houses.append((x, y))

    def plot(self, title= " ", file_name=None):
        fig, ax = plt.subplots()
        agent_colors = {1: 'b', 2: 'r', 3: 'g', 4: 'c', 5: 'm', 6: 'y', 7: 'k'}
        for agent in self.agents:
            ax.scatter(agent[0] + 0.5, agent[1] + 0.5, color=agent_colors[self.agents[agent]])
        ax.set_title(title, fontsize=10, fontweight='bold')
        ax.set_xlim([0, self.width])
        ax.set_ylim([0, self.height])
        ax.set_xticks([])
        ax.set_yticks([])
        fig.set_size_inches(8,8)
        plt.show()



class FastSchelling:
    def __init__(
        self,
        height: int,
        width: int,
        empty_ratio: float,
        similarity_threshold: float,
        n_iterations: int,
        types: int = 2,
    ) -> None:
        self.height = height
        self.width = width
        self.empty_ratio = empty_ratio
        self.similarity_threshold = similarity_threshold
        self.n_iterations = n_iterations

        self.kernel = np.ones((3, 3), dtype=np.uint8)
        self.kernel[1, 1] = 0

        self.state = np.zeros((types, height, width), dtype=self.kernel.dtype)
        # Populate state with agents
        locs = [*zip(*np.where(np.ones((height, width))))]
        np.random.shuffle(locs)
        locs = locs[int(empty_ratio * height * width) :]
        for i, (r, c) in enumerate(locs):
            t = i % types
            self.state[t, r, c] = 1

    def unsatisfied(self) -> np.ndarray:
        populated = self.state.sum(0)
        unsat = []
        for us in self.state:
            goods = scipy.signal.convolve(us, self.kernel, "same")
            alls = scipy.signal.convolve(populated, self.kernel, "same")
            ratios = goods / (alls + (alls == 0))
            unsat.append((ratios < self.similarity_threshold) & us)
        return np.stack(unsat)

    def step(self) -> int:
        unsat = self.unsatisfied()
        # Clear unsatisfied squares
        self.state -= unsat

        # Valid destinations
        dests = [*zip(*np.where(self.state.sum(0) == 0))]

        np.random.shuffle(dests)
        ts = sum([[i] * s for i, s in enumerate(unsat.sum((1, 2)))], [])
        for t, (r, c) in zip(ts, dests):
            self.state[t, r, c] = 1

        return unsat.sum()

    def go(self) -> list[int]:
        ys = []
        for _ in range(self.n_iterations):
            n_unsat = self.step()
            ys.append(n_unsat)
            if n_unsat == 0:
                break
        return ys

    def plot(self, title="Agents"):
        fig, ax = plt.subplots()
        colours = {0: "b", 1: "r", 2: "g", 3: "c", 4: "m", 5: "y", 6: "k"}
        for i, plane in enumerate(self.state):
            w0, w1 = np.where(plane)
            # Transpose row-col to x-y
            plt.scatter(w1 + 0.5, w0 + 0.5, c=colours[i])
        ax.set_title(title, fontsize=10, fontweight="bold")
        ax.set_xlim([0, self.width])
        ax.set_ylim([0, self.height])
        ax.set_xticks([])
        ax.set_yticks([])
        fig.set_size_inches(8, 8)
        plt.show()