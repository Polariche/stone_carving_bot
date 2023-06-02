
import random;
import numpy as np

upper_cap = 0.75
lower_cap = 0.25

def up_prob(x):
	return min(x+0.1, upper_cap)

def down_prob(x):
	return max(x-0.1, lower_cap)

def game():
	prob = upper_cap

	stones = np.array([[-1 for _ in range(10)] for _ in range(3)])
	idx = np.array([0,0,0])
	tries = 0

	tries_hist = []

	while (tries < 30):
		options = np.arange(3)[idx < 10]

		choose = random.choice(options)	# replace with user input
		tries_hist.append(choose)
		dice = random.random()

		if (dice < prob):	# success
			prob = down_prob(prob)
			stones[choose][idx[choose]] = 1

		else:	# failure
			prob = up_prob(prob)
			stones[choose][idx[choose]] = 0

		idx[choose] += 1
		tries += 1

	print(tries_hist)
	print(stones)
	print(np.sum(stones, axis=1))

game()