"""                                                                                               
A simple wrapper for linear regression.  (c) 2015 Tucker Balch                                                                                                
                                                                                              
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
                                                                                              
import numpy as np                                                                                          

class DTLearner(object):                                                                                              
                                                                                              
    def __init__(self, leaf_size=1, verbose=False):
        self.leafSize = leaf_size
        self.verbose = verbose      
        self.tree = None

    def author(self):                                                                                             
        return 'czheng71' # replace tb34 with your Georgia Tech username                                                                                              
    
    def buildTree(self, dataX, dataY):
        if dataX.shape[0] <= self.leafSize:
            #only one data
            return np.array([[np.nan, dataY.mean(), np.nan, np.nan]])
        if np.unique(dataY).shape[0] == 1:
            #no unique response
            return np.array([[np.nan, dataY[0], np.nan, np.nan]])
        #get the highest correlation of all features
        corrsRes = np.apply_along_axis(lambda a: abs(np.corrcoef(a, dataY)[0,1]), 1, dataX.T)
        selFeat = np.argmax(corrsRes)
        #compute the median for that feature
        medVal = np.median(dataX[:, selFeat])
        maxVal = np.max(dataX[:, selFeat])
        #median equals max, the split would recurse forever if continued
        #return the mean of the y here
        if medVal == maxVal:
            return np.array([[np.nan, np.mean(dataY), np.nan, np.nan]]) 
        #create mask for splitting data
        leftMask = dataX[:,selFeat] <= medVal
        rightMask = np.invert(leftMask)
        #call recursively on both sides
        leftTree = self.buildTree(dataX[leftMask], dataY[leftMask])
        rightTree = self.buildTree(dataX[rightMask], dataY[rightMask])
        #create current node
        curNode = np.array([[selFeat, medVal, 1, leftTree.shape[0] + 1]])
        return np.concatenate((curNode, leftTree, rightTree), axis=0)

    def addEvidence(self,dataX,dataY):                                                                                                
        """                                                                                               
        @summary: Add training data to learner                                                                                                
        @param dataX: X values of data to add                                                                                             
        @param dataY: the Y training values                                                                                               
        """     
        self.tree = self.buildTree(dataX, dataY)     

    def queryTree(self, point, tree):
        feature, split, left, right = tree[0]
        if np.isnan(feature):
            #leaf node
            return split
        #convert to integers...
        feature, left, right = int(feature), int(left), int(right)
        #not leaf node, compare the feature
        if point[feature] <= split:
            #go to left
            return self.queryTree(point, tree[left:right])
        else:
            return self.queryTree(point, tree[right:])
                                      
    def query(self, points):                                                                                               
        """                                                                                               
        @summary: Estimate a set of test points given the model we built.                                                                                             
        @param points: should be a numpy array with each row corresponding to a specific query.                                                                                               
        @returns the estimated values according to the saved model.                                                                                               
        """
        return np.apply_along_axis(lambda a: self.queryTree(a, self.tree), 1, points)                                                                                                
                                                                                              
if __name__=="__main__": 
    print "the secret clue is 'zzyzx'"           