"""
template for generating data to fool learners (c) 2016 Tucker Balch
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
import math

# this function should return a dataset (X and Y) that will work
# better for linear regression than decision trees
def best4LinReg(seed=1489683273):
    np.random.seed(seed)
    # X = np.zeros((100,2))

    x1 = np.random.normal(0,1,size=100)
    x2 = np.random.uniform(1,50,size= 100)
    x3 = np.random.normal(10,1,size=100) + 3
    x4 = np.random.normal(9,1,size=100) - 20
    x5 = np.random.uniform(-9,10,size=100) +9.9

    X = np.vstack([x1,x2,x3,x4,x5]).T

    # Here's is an example of creating a Y from randomly generated
    # X with multiple columns
    Y = X[:,0] + 3*X[:,1] - 2*X[:,2] + 19*X[:,3] -2*X[:,4]
    return X, Y

def best4DT(seed=1489683273):
    np.random.seed(seed)

    x1 = np.random.normal(1, 2, size=100)
    x2 = np.random.uniform(1, 5, size=100)
    x3 = np.sin(np.random.normal(2, 10, size=100) + 3)
    x4 = np.random.normal(9, 1, size=100) - 20
    x5 = np.random.normal(7.8, 0.7, size=100) + 9.9
    X = np.vstack([x1, x2, x3, x4, x5]).T


    # Here's is an example of creating a Y from randomly generated
    # X with multiple columns
    Y = X[:, 0]**2 + np.sqrt(X[:, 1]) - np.exp(X[:, 2]) +  np.e**(X[:, 3]) - np.cos(X[:, 4]) + X[:, 1]*X[:, 2] - 78
    return X, Y


def author():
    return 'lzheng73' #Change this to your user ID

if __name__=="__main__":
    print "they call me Tim."
