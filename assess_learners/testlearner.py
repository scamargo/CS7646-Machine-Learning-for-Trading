""""""
"""
Test a learner.  (c) 2015 Tucker Balch

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
"""

import math
# import sys
import os.path as path

import numpy as np
import pandas as pd
import LinRegLearner as lrl
import DTLearner as dtl

def importData(dataFileName = None):
    # if len(sys.argv) == 1 and isinstance(dataFileName, str):
    #     inf = open(dataFileName)
    # elif len(sys.argv) == 2:
    #     # inf = open(sys.argv[1])
    # else:
    #     print("Usage: python testlearner.py <filename>")
    #     sys.exit(1)
        
    izzy = 'Data/Istanbul.csv'
    if dataFileName == izzy:
        file_name = 'Istanbul'
        df = pd.read_csv('{}/{}.csv'.format(path.abspath(path.join(__file__, '../Data')), file_name), index_col=['date'], parse_dates=True)
        data = df.to_numpy()
    else:
        inf = open(dataFileName)
        data = np.array( [list(map(float, s.strip().split(","))) for s in inf.readlines()] )
    return data


def testTrainSplit(data, train_size = 0.6):
    # compute how much of the data is training and testing
    train_rows = int(train_size * data.shape[0])
        # test_rows = data.shape[0] - train_rows
    # separate out training and testing data
    train_x = data[:train_rows, 0:-1]
    train_y = data[:train_rows, -1]
    test_x = data[train_rows:, 0:-1]
    test_y = data[train_rows:, -1]
    return train_x, train_y, test_x, test_y


def trainLearner(learner, train_x, train_y):
    
    # create a learner and train it
    learner.add_evidence(train_x, train_y)  # train it

    # evaluate in sample
    pred_y = learner.query(train_x)  # get the predictions
    rmse = math.sqrt(((train_y - pred_y) ** 2).sum() / train_y.shape[0])
    
    print("In sample results")
    print(f"\tShape of train_x: {train_x.shape}")
    print(f"\tShape of train_y: {train_y.shape}")
    print(f"\tRMSE: {np.array(rmse).round(3)}")
    c = np.corrcoef(pred_y, y=train_y)
    print(f"\tcorr: {np.array(c[0,1]).round(3)}")
    return learner


def testLearner(learner, test_x, test_y):
    
    # evaluate out of sample
    pred_y = learner.query(test_x)  # get the predictions
    rmse = math.sqrt(((test_y - pred_y) ** 2).sum() / test_y.shape[0])
    
    print("Out of sample results")
    print(f"\tShape of test_x: {test_x.shape}")
    print(f"\tShape of test_y: {test_y.shape}")
    print(f"\tRMSE: {np.array(rmse).round(3)}")
    c = np.corrcoef(pred_y, y=test_y)
    print(f"\tcorr: {np.array(c[0,1]).round(3)}")
    
    
def mlRoutine(learner, dataSets = None):
    
    dataDict = {}
    dataDict['3_groups'] = 'Data/3_groups.csv'
    dataDict['Istanbul'] = 'Data/Istanbul.csv' # not working, first column (date) is causing problems upon import attemp
    dataDict['ripple'] = 'Data/ripple.csv'
    dataDict['simple'] = 'Data/simple.csv'
    dataDict['winequality-red'] = 'Data/winequality-red.csv'
    dataDict['winequality-white'] = 'Data/winequality-white.csv'
    
    print()
    print('Author: ' + learner.author())
    
    for dataFileKey in dataSets:
        
        print()
        print(dataFileKey)
        
        dataFile = dataDict[dataFileKey]
        
        data = importData(dataFile)
        train_x, train_y, test_x, test_y = testTrainSplit(data, train_size = 0.6)
        learner = trainLearner(learner, train_x, train_y)
        print()
        testLearner(learner, test_x, test_y)

if __name__ == "__main__":
    
    # TODO: loop over every learner?
    
    # learner = lrl.LinRegLearner(verbose=True)  # create a LinRegLearner
    learner = dtl.DTLearner(leaf_size = 1, verbose=True)  # create a DTLearner
    
    dataSets = ['Istanbul'] # ['3_groups', 'Istanbul', 'ripple', 'simple', 'winequality-red', 'winequality-white']
    
    mlRoutine(learner, dataSets)
