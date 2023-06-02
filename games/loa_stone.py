
import random;
import numpy as np

upper_cap = 75
lower_cap = 25

class LOA_Stone():

    def __init__(self):
        self.reset()

    def reset(self):
        self.prob = upper_cap
        self.stones = -np.ones((3,10), dtype=np.int8)

        self.tries_hist = []

    def up_prob(self):
        self.prob = min(self.prob+10, upper_cap)

    def down_prob(self):
        self.prob = max(self.prob-10, lower_cap)

    def tries(self):
        return np.sum(self.stones > -1, axis=1)

    def tries_slot(self, slot):
        return np.sum(self.stones[slot] > -1, axis=1)

    def tries_total(self):
        return np.sum(self.stones > -1)

    def max_tries(self):
        return self.stones.size

    def options(self):
        return np.arange(3)[self.tries() < 10]

    
    def try_option(self, choice):

        # if no more tries left
        if self.tries_total() >= self.max_tries():
            return False

        # validate our choice
        if choice not in self.options():
            return False

        idx = self.tries()

        dice = random.random()

        if (dice*100 < self.prob):   # success
            self.down_prob()
            self.stones[choice][idx[choice]] = 1

        else:   # failure
            self.up_prob()
            self.stones[choice][idx[choice]] = 0

        self.tries_hist.append(choice)

        return True

    def result(self):
        stone_done = self.stones.copy()
        stone_done[stone_done < 0] = 0
        return np.sum(stone_done, axis=1)

def game():
    stonegame = LOA_Stone()

    while (stonegame.tries_total() < 30):
        options = stonegame.options()
        choice = random.choice(options) # replace with user input
        stonegame.try_option(choice)

    return [stonegame.tries_hist
            ,stonegame.stones
            ,stonegame.result()]


if __name__ == "__main__":

    results = game()

    for r in results:
        print(r)