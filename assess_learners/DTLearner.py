import numpy as np  		  	   		   	 			  		 			     			  	  		 	  	 		 			  		  			
  		  	   		   	 			  		 			     			  	  		 	  	 		 			  		  			
LEAF = -1
NA = -1  		  	   		   	 			  		 			     			  	  		 	  	 		 			  		  			
class DTLearner(object):  		  	   		   	 			  		 			     			  	  		 	  	 		 			  		  			
    """  		  	   		   	 			  		 			     			  	  		 	  	 		 			  		  			
    This is a Decision Tree Learner. It is perhaps implemented correctly.  		  	   		   	 			  		 			     			  	  		 	  	 		 			  		  			
  		  	   		   	 			  		 			     			  	  		 	  	 		 			  		  			
    :param verbose: If “verbose” is True, your code can print out information for debugging.  		  	   		   	 			  		 			     			  	  		 	  	 		 			  		  			
        If verbose = False your code should not generate ANY output. When we test your code, verbose will be False.  		  	   		   	 			  		 			     			  	  		 	  	 		 			  		  			
    :type verbose: bool  		  	   		   	 			  		 			     			  	  		 	  	 		 			  		  			
    """  		  	   		   	 			  		 			     			  	  		 	  	 		 			  		  			
    def __init__(self, leaf_size=1, verbose=False):  		  	   		   	 			  		 			     			  	  		 	  	 		 			  		  			
        """  		  	   		   	 			  		 			     			  	  		 	  	 		 			  		  			
        Constructor method		  	   		   	 			  		 			     			  	  		 	  	 		 			  		  			
        """  		  	   		   	 			  		 			     			  	  		 	  	 		 			  		  			
        self.verbose = verbose
        self.leaf_size = leaf_size		  	   		   	 			  		 			     			  	  		 	  	 		 			  		  			
  		  	   		   	 			  		 			     			  	  		 	  	 		 			  		  			
    def author(self):  		  	   		   	 			  		 			     			  	  		 	  	 		 			  		  			
        """  		  	   		   	 			  		 			     			  	  		 	  	 		 			  		  			
        :return: The GT username of the student  		  	   		   	 			  		 			     			  	  		 	  	 		 			  		  			
        :rtype: str  		  	   		   	 			  		 			     			  	  		 	  	 		 			  		  			
        """  		  	   		   	 			  		 			     			  	  		 	  	 		 			  		  			
        return "tb34"  # replace tb34 with your Georgia Tech username

    def append(self, root, lefttree, righttree):
        # join root, lefttree, and righttree
        tree = np.append(root, lefttree)
        return np.append(tree, righttree)

    def split_feature(self, data_x, data_y):
        # return axis of feature with highest correlation to y
        correlations = np.ones(np.shape(data_x[1]))
        for i in range(np.shape(data_x)[1]):
            correlations[i] = np.corrcoef(data_x[:,i],data_y)[0,1] # check this is getting you a valid corr
        return np.nanargmax(np.absolute(correlations)) # return index of largest correlation
    
    def build_tree(self, data_x, data_y):
        if self.verbose: print("np.shape(data_x)[0]: {}".format(np.shape(data_x)[0]))
        if np.shape(data_x)[0] <= self.leaf_size:
            if self.verbose: print("ROWS <= LEAF SIZE") 
            return [LEAF, np.mean(data_y), NA, NA]
        if np.all(data_y == data_y[0]): return [LEAF, data_y, NA, NA]
        
        i = self.split_feature(data_x, data_y)
        split_val = np.median(data_x[:,i])
        if self.verbose:
            if np.shape(data_x)[0] == 2:
                print("split_val: {}".format(split_val))
                print("data_x[:,i]: {}".format(data_x[:,i]))
        lefttree = self.build_tree(data_x[data_x[:,i]<=split_val], data_y[data_x[:,i]<=split_val])
        righttree = self.build_tree(data_x[data_x[:,i]>split_val], data_y[data_x[:,i]>split_val])
        root = [i, split_val, 1, np.shape(lefttree)[0] + 1]
        return (self.append(root, lefttree, righttree))	  	   		   	 			  		 			     			  	  		 	  	 		 			  		  			
  		  	   		   	 			  		 			     			  	  		 	  	 		 			  		  			
    def add_evidence(self, data_x, data_y):  		  	   		   	 			  		 			     			  	  		 	  	 		 			  		  			
        """  		  	   		   	 			  		 			     			  	  		 	  	 		 			  		  			
        Add training data to learner  		  	   		   	 			  		 			     			  	  		 	  	 		 			  		  			
  		  	   		   	 			  		 			     			  	  		 	  	 		 			  		  			
        :param data_x: A set of feature values used to train the learner  		  	   		   	 			  		 			     			  	  		 	  	 		 			  		  			
        :type data_x: numpy.ndarray  		  	   		   	 			  		 			     			  	  		 	  	 		 			  		  			
        :param data_y: The value we are attempting to predict given the X data  		  	   		   	 			  		 			     			  	  		 	  	 		 			  		  			
        :type data_y: numpy.ndarray  		  	   		   	 			  		 			     			  	  		 	  	 		 			  		  			
        """  		  	   		   	 			  		 			     			  	  		 	  	 		 			  		  			
    
        # build tree
        self.tree = self.build_tree(data_x, data_y)
        return
    
    # TODO: parse through decision tree to return answer
    def query(self, points):  		  	   		   	 			  		 			     			  	  		 	  	 		 			  		  			
        """  		  	   		   	 			  		 			     			  	  		 	  	 		 			  		  			
        Estimate a set of test points given the model we built.  		  	   		   	 			  		 			     			  	  		 	  	 		 			  		  			
  		  	   		   	 			  		 			     			  	  		 	  	 		 			  		  			
        :param points: A numpy array with each row corresponding to a specific query.  		  	   		   	 			  		 			     			  	  		 	  	 		 			  		  			
        :type points: numpy.ndarray  		  	   		   	 			  		 			     			  	  		 	  	 		 			  		  			
        :return: The predicted result of the input data according to the trained model  		  	   		   	 			  		 			     			  	  		 	  	 		 			  		  			
        :rtype: numpy.ndarray  		  	   		   	 			  		 			     			  	  		 	  	 		 			  		  			
        """  		  	   		   	 			  		 			     			  	  		 	  	 		 			  		  			
        #result = 
        #for i in np.shape(points)[1]:

        return 1	  	   		   	 			  		 			     			  	  		 	  	 		 			  		  				  	   		   	 			  		 			     			  	  		 	  	 		 			  		  			
  		  	   		   	 			  		 			     			  	  		 	  	 		 			  		  			
  		  	   		   	 			  		 			     			  	  		 	  	 		 			  		  			
if __name__ == "__main__":  		  	   		   	 			  		 			     			  	  		 	  	 		 			  		  			
    print("the secret clue is 'zzyzx'")  	