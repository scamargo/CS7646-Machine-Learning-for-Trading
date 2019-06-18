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
  		   	  			    		  		  		    	 		 		   		 		  
import numpy as np  		   	  			    		  		  		    	 		 		   		 		  
import math  		   	  			    		  		  		    	 		 		   		 		  
import LinRegLearner as lrl
import pandas as pd
import sys
import DTLearner as dt
import matplotlib.pyplot as plt
import BagLearner as bg
import RTLearner as rtl
  		   	  			    		  		  		    	 		 		   		 		  
if __name__=="__main__":  		   	  			    		  		  		    	 		 		   		 		  
#    if len(sys.argv) != 2:  		   	  			    		  		  		    	 		 		   		 		  
#        print "Usage: python testlearner.py <filename>"  		   	  			    		  		  		    	 		 		   		 		  
    inf = sys.argv[1]
    data = np.array(pd.read_csv(inf))
    data = data[:,1:]
#    print data
  		   	  			    		  		  		    	 		 		   		 		  
    # compute how much of the data is training and testing  		   	  			    		  		  		    	 		 		   		 		  
    train_rows = int(0.6* data.shape[0])  		   	  			    		  		  		    	 		 		   		 		  
    test_rows = data.shape[0] - train_rows  		   	  			    		  		  		    	 		 		   		 		  
  		   	  			    		  		  		    	 		 		   		 		  
    # separate out training and testing data  		   	  			    		  		  		    	 		 		   		 		  
    trainX = data[:train_rows,0:-1]  		   	  			    		  		  		    	 		 		   		 		  
    trainY = data[:train_rows,-1]
    testX = data[train_rows:,0:-1]  		   	  			    		  		  		    	 		 		   		 		  
    testY = data[train_rows:,-1]  		   	  			    		  		  		    	 		 		   		 		  
  		   	  			    		  		  		    	 		 		   		 		  
    # print testX.shape
    # print testY.shape
    # ===========================================Linear Learner=========================
    # create a learner and train it  		   	  			    		  		  		    	 		 		   		 		  
    learner = lrl.LinRegLearner(verbose = True) # create a LinRegLearner
    learner.addEvidence(trainX, trainY) # train it
    # print learner.author()

    # evaluate in sample
    predY = learner.query(trainX) # get the predictions
    rmse = math.sqrt(((trainY - predY) ** 2).sum()/trainY.shape[0])
    print "In sample results"
    print "RMSE: ", rmse

#    print predY, trainY
    c = np.corrcoef(predY.astype('float'), y=trainY.astype('float'))
    print "corr: ", c[0,1]

    # evaluate out of sample
    predY = learner.query(testX) # get the predictions
    rmse = math.sqrt(((testY - predY) ** 2).sum()/testY.shape[0])
    print "Out of sample results"
    print "RMSE: ", rmse
    c = np.corrcoef(predY.astype('float'), y=testY.astype('float'))
    print "corr: ", c[0,1]

# =================DT Learner=================================
#     print trainX
#     print trainY



    # the bigger leaf-size is, the fewer the number of leaf is, the more likely
    # underfitting happen
    rmse_dt_in = []
    rmse_dt_out = []
    rmse_bg_in = []
    rmse_bg_out = []
    rmse_rt_in = []
    rmse_rt_out = []
    leaf_num_dt = []
    leaf_num_rt = []
    node_num_dt = []
    node_num_rt = []
    leaf_range = range(1,100)
    for leaf_size in leaf_range:
        print leaf_size
        # Decision tree

        learner_dt = dt.DTLearner(leaf_size = leaf_size, verbose = False)
        learner_dt.addEvidence(trainX,trainY)
        predY_in = learner_dt.query(trainX)  # get the predictions
        rmse_in = math.sqrt(((trainY - predY_in) ** 2).sum() / trainY.shape[0])
        predY_out = learner_dt.query(testX)
        rmse_out = math.sqrt(((testY - predY_out) ** 2).sum()/testY.shape[0])
        rmse_dt_in.append(rmse_in)
        rmse_dt_out.append(rmse_out)

        leaf_num_dt.append((learner_dt.learner[:, 0] == 'leaf').sum())
        node_num_dt.append(len(learner_dt.learner))

        # Random tree
        learner_rt = rtl.RTLearner(leaf_size = leaf_size, verbose = False)
        learner_rt.addEvidence(trainX,trainY)
        predY_in = learner_rt.query(trainX)  # get the predictions
        rmse_in = math.sqrt(((trainY - predY_in) ** 2).sum() / trainY.shape[0])
        predY_out = learner_rt.query(testX)
        rmse_out = math.sqrt(((testY - predY_out) ** 2).sum()/testY.shape[0])
        rmse_rt_in.append(rmse_in)
        rmse_rt_out.append(rmse_out)
        leaf_num_rt.append((learner_rt.learner[:, 0] == 'leaf').sum())
        node_num_rt.append(len(learner_rt.learner))


        # Bagging
        learner_bag = bg.BagLearner(learner = dt.DTLearner,kwargs={'leaf_size':leaf_size,'verbose':False},bags=20,boost=False,verbose=False)
        learner_bag.addEvidence(trainX,trainY)
        predY_in = learner_bag.query(trainX)
        predY_out = learner_bag.query(testX)
        rmse_in = math.sqrt(((trainY - predY_in) ** 2).sum() / trainY.shape[0])
        rmse_out = math.sqrt(((testY - predY_out) ** 2).sum()/testY.shape[0])
        rmse_bg_in.append(rmse_in)
        rmse_bg_out.append(rmse_out)


    # Decision tree plot

    fig = plt.figure(1)
    plt.plot(leaf_range, rmse_dt_in,label = 'dt-in_sample')
    plt.plot(leaf_range, rmse_dt_out,label = 'dt-out_sample')
    plt.grid(True,alpha = 0.5)
    plt.legend(loc = 'best')
    plt.xlabel('Leaf Size')
    plt.ylabel('RMSE')
    plt.title('DTLearner RMSE')
    fig.save('figure1.png')
    

    fig = plt.figure(2)
    plt.plot(leaf_range, rmse_rt_in, label = 'rt-in_sample')
    plt.plot(leaf_range, rmse_rt_out, label = 'rt-out_sample')
    plt.grid(True,alpha = 0.5)
    plt.legend(loc = 'best')
    plt.xlabel('Leaf Size')
    plt.ylabel('RMSE')
    plt.title('RTLearner RMSE')
    fig.save('figure2.png')

    
    
    #

    # print leaf_num
    # # leaf number plot
    fig = plt.figure(3)
    plt.figure(3)
    plt.plot(leaf_range, leaf_num_dt, label = 'dt-leaf_num')
    plt.plot(leaf_range, leaf_num_rt, label = 'rt-leaf_num')
    plt.grid(True, alpha=0.5)
    plt.legend(loc = 'best')
    plt.xlabel('Leaf Size')
    plt.ylabel('Leaf Number')
    plt.title('Leaf Number of A Tree')
    fig.save('figure3.png')

    # Node number
    # m = np.log2(node_num_rt+1)

    # depth_rt = map(int, np.log2(node_num_rt+1))
    # depth_dt = map(int, np.log2(node_num_dt+1))
    # plt.figure(3)
    # plt.plot(leaf_range, node_num_dt, label='dt-node_num')
    # plt.plot(leaf_range, node_num_rt, label='rt-node_num')
    # plt.grid(True, alpha=0.5)
    # plt.legend(loc='best')
    # plt.xlabel('Leaf Size')
    # plt.ylabel('node Number')
    # plt.title('node Number of A Tree')



    # Bagging plot
    fig = plt.figure(4)
    plt.figure(4)
    plt.grid(True,alpha = 0.5)
    plt.plot(leaf_range, rmse_bg_in, label = 'in-sample')
    plt.plot(leaf_range, rmse_bg_out, label = 'out-sample')
    plt.legend(loc = 'best')
    plt.xlabel('Leaf Size')
    plt.ylabel('RMSE')
    plt.title('BagLearner RMSE')
    fig.save('figure4.png')


