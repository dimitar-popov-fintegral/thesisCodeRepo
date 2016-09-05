# coding=utf-8

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

def runQuadOptimizer_globalMinVar(matSigma):
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
    A = matrix(np.ones(shape=(1, n)), tc='d')
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