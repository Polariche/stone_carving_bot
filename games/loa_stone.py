
import random;
import numpy as np
from games.game import Game

upper_cap = 75
lower_cap = 25

class LOA_Stone(Game):

    def __init__(self, guild, user, permission, permission_user):
        super().__init__(guild, user, permission, permission_user)

        self.option_emojis = {"1️⃣":0, "2️⃣":1, "3️⃣":2, '🖕': 'quit'}
        self.reset()

    def emoji_to_option(self, emoji):
        return self.option_emojis[str(emoji)]

    def reset(self):
        self.prob = upper_cap
        self.stones = -np.ones((3,10), dtype=np.int8)

        self.tries_hist = []
        self.display_id = -1

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

    def available_options(self):
        return np.arange(3)[self.tries() < 10]

    def is_game_over(self):
        return self.tries_total() >= self.max_tries()
    
    def play_option(self, choice):
        if choice == 'quit':
            self.reset()
            return True

        # if no more tries left
        if self.is_game_over():
            return False

        # validate our choice
        if choice not in self.available_options():
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

    def generate_display_text(self):
        emojis = [":black_medium_small_square:",
                       ":small_blue_diamond:",
                       ":small_orange_diamond:",
                       "◇"]

        result = self.result()

        stones = self.stones.copy()
        stones[2][stones[2] > 0] = 2
        stones[stones < 0] = 3

        mention_display = f'<@{self.user_id}>'

        if self.permission == "이사람만" and self.permission_user_id != self.user_id:
            mention_display += f' <@{self.permission_user_id}>' 

        display = '\n'.join([' '.join([emojis[c] for c in s]) for i,s in enumerate(stones)])
        result_display = f"{result[0]}/{result[1]}/{result[2]} 돌을 깎으셨습니다."

        display = mention_display + "\n" + display + "\n" + result_display

        if (self.tries_total() < self.max_tries()):
            prob_display = f"현재 확률: {self.prob}%"
            display += " " + prob_display

        return display