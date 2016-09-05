# coding=utf-8

# temp
import sys
sys.path.extend(['/Users/Dim/Desktop/school_folder/masters_thesis/gitCodeRepo/codePython/collateralOptimizer/'])

# @date: 20160902
# @author: DA Popov
# @note: given recent difficulties in implementing the solver KNITRO, it was decided to attempt use of an alternative

## Imports
import numpy as np
import pandas as pd
from cvxopt import matrix
from cvxopt import solvers
from sklearn.covariance import *
from rollingCovarianceEstimation import *

## Functions
def runQuadOptimizer(matSigma):
    vecVola  = np.sqrt(matSigma.diagonal())
    n        = vecVola.shape[0]

    # Check for postive definite covariance matrix, if not exit
    if np.all(np.linalg.eigvals(matSigma) > 0) == False:
        print "Sigma matrix not positive definite, solution may not be unique! \nProceed Checking for semi-definiteness\n"
        if np.all(np.linalg.eigvals(matSigma) >= 0) == False:
            print "Sigma matrix not positive semi-definite!"
            raise SystemExit

    # Parameterize solver, using standard notation for cvxopt
    P = matrix(matSigma,tc='d')
    q = matrix(np.zeros(shape=(n, 1)), tc='d')
    G = matrix(np.diag(np.repeat(a=-1, repeats=n)), tc='d')
    g = matrix(np.zeros(shape=(n, 1)), tc='d')
    A = matrix(vecVola.reshape(1,n), tc='d')
    a = matrix(np.array([1]), tc='d')

    # Invoke solver
    sol = solvers.qp(A=A, b=a, G=G, h=g, P=P, q=q)

    # Solution
    xOpt = np.array(sol['x'])
    fOpt = np.array(sol['primal objective'])

    # Solution rescaled
    normalFactor = sum(xOpt)
    xOptScaled   = np.asarray(xOpt) * (1/normalFactor)

    return {'xOpt':xOpt, 'xOptScaled':xOptScaled, 'fOpt':fOpt}

# ## Main
# # Set path & get rolling covariance estimate (MLE only at this stage!)
# filePath = '/Users/Dim/Desktop/school_folder/masters_thesis/gitCodeRepo/data/noStaleX_returnsData_20160825.csv'
# winSize  = 250
# rollObj  = getRollingCovariance(filePath=filePath, winSize=winSize)
# r        = rollObj['rollCov']
# df       = rollObj['df']
#
# # Select rolling covariance matrices
# s = r[df.index[range(winSize, df.shape[0], winSize)]]
# print "#!# Done with data-prep #!#\n"
#
# # Feed rolling covariance matrices into solver
# bucket = pd.DataFrame(index=range(0, df.shape[1]), data=range(0, df.shape[1]), columns=['test'])
# for item in s:
#     container = runQuadOptimizer(r[item].as_matrix())
#     fill      =  pd.DataFrame(data=container['xOptScaled'], columns=[item])
#     bucket = pd.concat([bucket, fill], axis=1)
#     #bucket.append(container['xOptScaled'])
#
# bucket = bucket.drop('test', axis=1)
# historicalWeights = bucket
# del bucket
