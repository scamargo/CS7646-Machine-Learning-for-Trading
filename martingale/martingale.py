"""Assess a betting strategy.

Copyright 2018, Georgia Institute of Technology (Georgia Tech)
Atlanta, Georgia 30332
All Rights Reserved

Template code for CS 4646/7646

Georgia Tech asserts copyright ownership of this template and all derivative
works, including solutions to the projects assigned in this course. Students
and other users of this template code are advised not to share it with others
or to make it available on publicly viewable websites including repositories
such as github and gitlab.  This copyright statement should not be removed
or edited.

We do grant permission to share solutions privately with non-students such
as potential employers. However, sharing with other current or future
students of CS 7646 is prohibited and subject to being investigated as a
GT honor code violation.

-----do not edit anything above this line---

Student Name: Lu Zheng (replace with your name)
GT User ID: lzheng73 (replace with your User ID)
GT ID: 903438769 (replace with your GT ID)
"""

import numpy as np
import matplotlib.pyplot as plt

def author():
	return 'lzheng73' # replace tb34 with your Georgia Tech username.

def gtid():
	return 903438769 # replace with your GT ID number

def get_spin_result(win_prob):
	result = False
	if np.random.random() <= win_prob:
		result = True
	return result
    
# if unlimited capital, then bankroll<0
def test_code(bank_roll, win_prob):
	# print get_spin_result(win_prob)  # test the roulette spin
	winnings = np.zeros(1000)
	episode_winnings = 0
	bet_amount = 1
	trail_count = 0
	if bank_roll<0:
		while episode_winnings<80:
			if trail_count >= 1000:
				break
			won = get_spin_result(win_prob)

			if won:
				episode_winnings = episode_winnings + bet_amount
				bet_amount = 1

			else:
				episode_winnings = episode_winnings - bet_amount
				bet_amount = bet_amount*2
			winnings[trail_count] = episode_winnings
			trail_count = trail_count+1
		winnings[trail_count:] = 80
		return winnings
	else:
		while episode_winnings < 80:
			if trail_count >=  1000:
				break
			won = get_spin_result(win_prob)

			if won:
				episode_winnings = episode_winnings + bet_amount
				bank_roll = bank_roll + bet_amount
				bet_amount = 1

			else:
				episode_winnings = episode_winnings - bet_amount
				bank_roll = bank_roll - bet_amount
				if bank_roll > bet_amount * 2:
					bet_amount = bet_amount * 2
				elif bank_roll > 0:
					bet_amount = bank_roll
				else:
					winnings[trail_count:] = episode_winnings
					return winnings

			winnings[trail_count] = episode_winnings
			trail_count = trail_count + 1

		winnings[trail_count:] = 80

		return winnings

np.random.seed(gtid())  # do this only once

# add your code here to implement the experiments

if __name__ == "__main__":
	prob = 9/19.0

	n = 1000

	# Experiment 1
	# Figure1
	plt.figure(1)
	plt.grid(True)
	graph_data_Ep0 = np.zeros(1000)
	plt.ylim([-256, 100])
	plt.xlim([0, 300])
	plt.grid(True)
	plt.title('Experiment 1_Figure1')
	plt.xlabel('#Trail')
	plt.ylabel('Episode_winnings')
	for i in range(10):
		graph_data = test_code(-1,prob)
		plt.plot(graph_data)
		graph_data_Ep0 = np.vstack([graph_data_Ep0, graph_data])
	graph_data_Ep0 = graph_data_Ep0[1:1001]
	plt.savefig("Figure1.png")

	# Figure 2
	plt.figure(2)
	plt.grid(True)
	plt.ylim([-256, 100])
	plt.xlim([0, 300])
	graph_data_Ep1 = np.zeros(1000)
	for i in range(n):
		graph_data1 = test_code(-1,prob)
		graph_data_Ep1 = np.vstack([graph_data_Ep1,graph_data1])
	plt.xlabel('#Trail')
	plt.ylabel('Episode_winnings')
	plt.title('Experiment 1_Figure2')
	graph_data_Ep1 = graph_data_Ep1[1:1001]

	mean_Ep1 = graph_data_Ep1.mean(axis=0)
	var_Ep1 = np.std(graph_data_Ep1, axis = 0)
	above_mean1 = mean_Ep1 + var_Ep1
	below_mean1 = mean_Ep1 - var_Ep1
	plt.plot(above_mean1, label='mean+var')
	plt.plot(mean_Ep1, label='mean')
	plt.plot(below_mean1, label='mean-var')
	plt.legend(loc = 'best')
	plt.savefig("Figure2.png")


	# Figure 3
	plt.figure(3)
	plt.grid(True)
	plt.xlim([0, 300])
	plt.ylim([-256, 100])
	plt.xlabel('#Trail')
	plt.ylabel('Episode_winnings')
	plt.title('Experiment 1_Figure3')
	median_Ep1 = np.median(graph_data_Ep1, axis=0)
	above_median1 = median_Ep1 + var_Ep1
	below_median1 = median_Ep1 - var_Ep1

	plt.plot(above_median1, label = 'median+var')
	plt.plot(median_Ep1, label = 'median')
	plt.plot(below_median1, label = 'median-var')
	plt.legend(loc = 'best')
	plt.savefig("Figure3.png")

	# Experiment 2
	# Figure 4
	plt.figure(4)
	plt.xlim([0,300])
	plt.ylim([-256,100])
	plt.grid(True)
	graph_data_Ep2 = np.zeros(1000)
	for i in range(n):
		graph_data2 = test_code(256,prob)
		graph_data_Ep2 = np.vstack([graph_data_Ep2,graph_data2])

	plt.xlabel('#Trail')
	plt.ylabel('Episode_winnings')
	plt.title('Experiment 2_Figure4')
	graph_data_Ep2 = graph_data_Ep2[1:1001]

	mean_Ep2 = graph_data_Ep2.mean(axis=0)
	var_Ep2 = np.std(graph_data_Ep2, axis=0)
	above_mean2 = mean_Ep2 + var_Ep2
	below_mean2 = mean_Ep2 - var_Ep2
	plt.plot(above_mean2, label='mean+var')
	plt.plot(mean_Ep2, label='mean')
	plt.plot(below_mean2, label='mean-var')
	plt.legend(loc = 'best')
	plt.savefig("Figure4.png")

	# Figure 5
	plt.figure(5)
	plt.xlim([0, 300])
	plt.grid(True)
	plt.ylim([-256, 100])
	plt.xlabel('#Trail')
	plt.ylabel('Episode_winnings')
	plt.title('Experiment 2_Figure5')
	median_Ep2 = np.median(graph_data_Ep2, axis=0)
	above_median2 = median_Ep2 + var_Ep2
	below_median2 = median_Ep2 - var_Ep2
	plt.plot(above_median2, label = 'median+var')
	plt.plot(median_Ep2, label = 'median')
	plt.plot(below_median2, label = 'median-var')
	plt.legend(loc = 'best')
	plt.savefig("Figure5.png")
