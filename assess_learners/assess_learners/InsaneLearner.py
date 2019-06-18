import numpy as np
import LinRegLearner as lrl
import BagLearner as bl

class InsaneLearner(object):
    bagLearner = None
    def __init__(self, verbose=False):
        self.verbose = verbose
        pass  # move along, these aren't the drones you're looking for

    def author(self):
        return 'lzheng73'  # replace tb34 with your Georgia Tech username

    def addEvidence(self, dataX, dataY):
        self.bagLearner = bl.BagLearner(learner=lrl.LinRegLearner,kwargs={},bags=20,boost=False,verbose=False)
        self.bagLearner.addEvidence(dataX,dataY)
        return self.bagLearner

    def query(self, points):
        return self.bagLearner.query(points)

