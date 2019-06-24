"""
Template for implementing QLearner  (c) 2015 Tucker Balch

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

Student Name: Tucker Balch (replace with your name)
GT User ID: tb34 (replace with your User ID)
GT ID: 900897987 (replace with your GT ID)
"""

import numpy as np
import random as rand

class QLearner(object):


    def __init__(self, \
        num_states=100, \
        num_actions = 4, \
        alpha = 0.2, \
        gamma = 0.9, \
        rar = 0.5, \
        radr = 0.99, \
        dyna = 0, \
        verbose = False):

        self.rar = rar
        self.radr = radr
        self.gamma = gamma
        self.alpha = alpha
        self.verbose = verbose
        self.num_actions = num_actions
        # s and a should be the current state and current action
        self.s = 0
        self.a = 0
        self.dyna = dyna
        self.Qtable = np.zeros((num_states,num_actions))
        self.experience_dic = {}

    def querysetstate(self, s):
        """
        @summary: Update the state without updating the Q-table
        @param s: The new state
        @returns: The selected action
        """
        random_int= np.random.binomial(1, self.rar)

        if random_int == 1:
            action = rand.randint(0, self.num_actions-1)
        else:
            action = self.Qtable[self.s].argmax()

        self.s = action

        if self.verbose: print "s =", s,"a =",action
        return action

    def query(self,s_prime,r):
        """
        @summary: Update the Q table and return an action
        @param s_prime: The new state
        @param r: the reward (float)
        @returns: The selected action
        """

        random_int= np.random.binomial(1, self.rar)

        # decide next action
        if random_int == 1:
            action = rand.randint(0, self.num_actions - 1)
        else:
            action = np.argmax(self.Qtable[s_prime])

        # update Q table
        new_estimate = r + self.gamma * self.Qtable[s_prime, action]
        self.Qtable[self.s, self.a] = (1-self.alpha) * self.Qtable[self.s, self.a]+ \
                self.alpha * new_estimate

        self.rar = self.rar * self.radr

        self.experience_dic[len(self.experience_dic)] = [self.s, self.a, s_prime, r]

        length = len(self.experience_dic)
        self.s = s_prime
        self.a = action
        if self.dyna != 0:
            for i in range(self.dyna):

                dyna_state, dyna_action, dyna_new_prime, R = self.experience_dic[rand.randint(0,length-1)]
                new_action = np.argmax(self.Qtable[dyna_new_prime])

                self.Qtable[dyna_state, dyna_action] = (1.0 - self.alpha) * self.Qtable[dyna_state, dyna_action] + \
                                                  self.alpha * (
                                                  R + self.gamma * self.Qtable[dyna_new_prime, new_action])
                self.s = s_prime
                self.a = action
        if self.verbose: print "s =", s_prime,"a =",action,"r =",r
        return action

    def author(self):
        return 'lzheng73'
if __name__=="__main__":
    print "Remember Q from Star Trek? Well, this isn't him"
