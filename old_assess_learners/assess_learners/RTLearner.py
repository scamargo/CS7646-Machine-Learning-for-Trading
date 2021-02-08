import numpy as np
import pandas as pd


class RTLearner(object):
    learner = None

    def __init__(self, leaf_size, verbose=False):
        self.leaf_size = leaf_size
        self.verbose = verbose
        pass  # move along, these aren't the drones you're looking for

    def author(self):
        return 'lzheng73'  # replace tb34 with your Georgia Tech username

    def addEvidence(self, dataX,dataY):
        """
        @summary: Add training data to learner
        @param dataX: X values of data to add
        @param dataY: the Y training values
        """
        dataY = dataY.reshape(dataY.shape[0], 1)
        data = np.hstack([dataX, dataY])

        shape = data.shape
        if data.shape[0] <= self.leaf_size:
            return np.array(['leaf', data[:, shape[1] - 1].mean(), np.nan, np.nan]).reshape(1, 4)
        elif len(set(data[:, shape[1] - 1])) == 1:
            return np.array(['leaf', data[:, shape[1] - 1].mean(), np.nan, np.nan]).reshape(1, 4)

        else:

            max_index = np.random.randint(shape[1]-1)
            splitVal = np.median(data[:, max_index])

            if splitVal == np.max(data[:, max_index]):
                return np.array(['leaf', data[:, shape[1] - 1].mean(), np.nan, np.nan]).reshape(1, 4)
            else:
                left_data = data[np.arange(shape[0])[data[:, max_index] <= splitVal]]
                right_data = data[np.arange(shape[0])[data[:, max_index] > splitVal]]

                left_dataX = left_data[:left_data.shape[0], 0:-1]
                left_dataY = left_data[:left_data.shape[0], -1]
                right_dataX = right_data[:right_data.shape[0], 0:-1]
                right_dataY = right_data[:right_data.shape[0], -1]

                left_tree = self.addEvidence(left_dataX,left_dataY)
                right_tree = self.addEvidence(right_dataX,right_dataY)
                self.learner = np.array([max_index, splitVal, 1, left_tree.shape[0] + 1]).reshape(1, 4)
                self.learner = np.vstack([self.learner, left_tree, right_tree])
                return self.learner


    def query_arr(self, model, points):

        if model[0][0] == 'leaf':
            return float(model[0][1])
        else:
            start_feature = int(float(model[0][0]))
            splitVal = float(model[0][1])
            left_index = int(float(model[0][2]))
            right_index = int(float(model[0][3]))
            if points[:, start_feature] <= splitVal:
                return self.query_arr(model[left_index:], points)
            else:
                return self.query_arr(model[right_index:], points)

    def query(self, test_data):
        pre = []
        for i in range(test_data.shape[0]):
            value = float(self.query_arr(self.learner, test_data[i].reshape(1, len(test_data[i]))))
            pre.append(value)
        return np.array(pre)

        # """
        # @summary: Estimate a set of test points given the model we built.
        # @param points: should be a numpy array with each row corresponding to a specific query.
        # @returns the estimated values according to the saved model.
        # """


# if __name__ == "__main__":
#     inf = open('Data/winequality-red.csv')
#     data = np.array(pd.read_excel('/users/zhenglu/desktop/test_tree_data.xlsx'))
#     test_data = np.array([[0.6, 0.3, 10.], [0.6, 0.3, 7.]])
#     learner = RTLearner(1, False)
#     print learner.addEvidence(data)
#     print learner.query(test_data)
#
#
#     "the secret clue is 'zzyzx'"
