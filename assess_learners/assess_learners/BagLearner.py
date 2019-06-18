import numpy as np


class BagLearner(object):
    self_learner_bag = []
    def __init__(self,learner,kwargs,bags,boost, verbose=False):
        self.learner = learner
        self.kwargs = kwargs
        self.bags = bags
        self.boost = boost
        self.verbose = verbose

        pass  # move along, these aren't the drones you're looking for

    def author(self):
        return 'lzheng73'  # replace tb34 with your Georgia Tech username

    def addEvidence(self, dataX, dataY):
        dataY = dataY.reshape(dataY.shape[0],1)
        data = np.hstack([dataX,dataY])
        shape = data.shape

        for i in range(self.bags):
            data_sample_index = np.random.choice(range(shape[0]),shape[0],replace=True)
            data_sample = data[data_sample_index]
            x = data_sample[:data_sample.shape[0], 0:-1]
            y = data_sample[:data_sample.shape[0], -1]
            learner_new = self.learner(**self.kwargs)
            learner_new.addEvidence(x, y)
            self.self_learner_bag.append(learner_new)
        return self.self_learner_bag

    def query(self, points):
        result = list(np.zeros(points.shape[0]))
        for i in self.self_learner_bag:

            result = np.vstack([result,i.query(points)])
        return result[1:].mean(axis=0)

# if __name__ == "__main__":
#     print "the secret clue is 'zzyzx'"
