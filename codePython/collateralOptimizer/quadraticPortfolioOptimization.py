# coding=utf-8

# import for solving division problem python2
from __future__ import division

## @file: quadraticPortfolioOptimization.py
## @author: DA POPOV
## @date:20160826
## @description: the purpose of this script is to call the KNITRO quadratic optimizer to solve portfolio optimizations

# standard imports
from knitro import *
import numpy as np
import pandas as pd
import re
from sklearn.covariance import LedoitWolf, empirical_covariance


# Function prepareProblem: this function constructs the variance-covariance matrix
# @param filePath:
# @param fileName:
# @param shrinkage: whether to apply the Ledoit, Wolf (2004) linear shrinkage estimator
def prepareProblem(filePath, shrinkage=False, subset=False, subsetSize=0):
    # Import data from .csv
    df = pd.read_csv(filePath, sep=';')
    df.index = df.date
    df = df.drop('date', axis=1)

    # Subset, if called via subset == True
    if subset == True:
        df = df.tail(subsetSize)

    # Estimate covariance using Empirical/MLE
    # Expected input is returns, hence set: assume_centered = True
    mleFitted = empirical_covariance(X=df, assume_centered=True)
    sigma = mleFitted

    if shrinkage == True:
        # Estimate covariance using LedoitWolf, first create instance of object
        lw = LedoitWolf(assume_centered=True)
        lwFitted = lw.fit(X=df).covariance_
        sigma = lwFitted

    return sigma

#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
#  Knitro example driver using reverse communications mode.
#
#  This executable invokes Knitro to solve a simple nonlinear
#  optimization test problem.  The purpose is to illustrate how to
#  invoke Knitro using the Python language API.
#
#  Before running, make sure ../../lib is in the load path.
#  To run:
#    python exampleQCQP
#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

#----------------------------------------------------------------
#   METHOD evaluateFC
#----------------------------------------------------------------
 ## Compute the function and constraint values at x.
 #
 #  For more information about the arguments, refer to the Knitro
 #  manual, especially the section on the Callable Library.
 ##
def evaluateFC (x, c):
    # Prepare funct. eval.
    #filePath = "/Users/Dim/Desktop/work_folder/six/code_CPP/SIX/csv/"
    #fileName = "threeAssetTestPortfolio.csv"
    #matSigma = prepareProblem(filePath=filePath, fileName=fileName)
    n = matSigma.shape[0]
    #vecOnes = np.ones(n)
    #vecVola = matSigma.diagonal()
    vecW = np.asarray(x)

    #---- OBJECTIVE FUNCTION.
    # dObj = np.transpose(vecW) * matSigma * vecW
    dObj = (1/2) * np.dot(np.transpose(vecW), np.dot(matSigma, vecW))

    #---- LINEAR EQUALITY CONSTRAINT.
    # c[0] = np.transpose(vecW) * vecVola
    c[0] = np.dot(np.transpose(vecW), vecVola)

    #---- LINEAR EQUALITY CONSTRAINT.
    # c[1] = np.transpose(vecW) * vecOnes
    # c[1] = np.dot(np.transpose(vecW), vecOnes)

    return dObj


#----------------------------------------------------------------
#   METHOD evaluateGA
#----------------------------------------------------------------
 ## Compute the function and constraint first deriviatives at x.
 #
 #  For more information about the arguments, refer to the Knitro
 #  manual, especially the section on the Callable Library.
 ##
def evaluateGA (x, objGrad, jac):
    # Prepare Jacobian eval.
    #filePath = "/Users/Dim/Desktop/work_folder/six/code_CPP/SIX/csv/"
    #fileName = "threeAssetTestPortfolio.csv"
    #matSigma = prepareProblem(filePath=filePath, fileName=fileName)
    n = matSigma.shape[0]
    #vecOnes = np.ones(n)
    #vecVola = matSigma.diagonal()
    vecW = np.asarray(x)
    dxObjective = np.dot(matSigma, vecW)

    for i in range(0, n):
        objGrad[i] = dxObjective[i]

    for i in range(0, n):
        jac[i] = vecVola[i]
        # jac[i + n] = vecOnes[i]

#----------------------------------------------------------------
#   METHOD evaluateH
#----------------------------------------------------------------
 ## Compute the Hessian of the Lagrangian at x and lambda.
 #
 #  For more information about the arguments, refer to the Knitro
 #  manual, especially the section on the Callable Library.
 ##
def evaluateH (x, lambda_, sigma, hess):
    # Prepare Hessian eval.
    #filePath = "/Users/Dim/Desktop/work_folder/six/code_CPP/SIX/csv/"
    #fileName = "threeAssetTestPortfolio.csv"
    #matSigma = prepareProblem(filePath=filePath, fileName=fileName)
    H = matSigma + np.transpose(matSigma)
    for i in range(0, n):
        for j in range(0, n):
            if j >= i:
                hess.append((sigma * H[i][j]))  # H[rows][cols]


#----------------------------------------------------------------
#   MAIN METHOD FOR TESTING
#----------------------------------------------------------------

#---- DEFINE THE OPTIMIZATION TEST PROBLEM.
#---- FOR MORE INFORMATION ABOUT THE PROBLEM DEFINITION, REFER
#---- TO THE KNITRO MANUAL, ESPECIALLY THE SECTION ON THE
#---- CALLABLE LIBRARY.

# read & construct data, matrices etc.
filePath = '/Users/Dim/Desktop/school_folder/masters_thesis/gitCodeRepo/data/noStaleX_returnsData_20160825.csv'
matSigma = prepareProblem(filePath=filePath, shrinkage=False, subset=True, subsetSize=120)
vecVola = np.sqrt(matSigma.diagonal())

# Check for postive definite covariance matrix, if not exit
if np.all(np.linalg.eigvals(matSigma) > 0) == False:
    print "Sigma matrix not positive definite!"
    raise SystemExit

# parametrize optimization problem
n = vecVola.size
m = 1
objGoal = KTR_OBJGOAL_MINIMIZE
objType = KTR_OBJTYPE_QUADRATIC;

# set bounds on objective
# ->> vecW
bndsLo = [0] * n
bndsUp = [KTR_INFBOUND] * n

# parametrize constraints
# ->> c[0]
# ->> c[1]
cType = [ KTR_CONTYPE_LINEAR ] #[ KTR_CONTYPE_LINEAR, KTR_CONTYPE_LINEAR ]
cBndsLo = [1] #[ 1, 1 ]
cBndsUp = [1] #[ 1, 1 ]

# parametrize derivatives
nnzJ = n * (m + 1) # Since Jac has constraint matrix non-zero (n * m) as well as Objective matrix non-zero (n)
nnzH = int((n * (n + 1)) / 2) # Since Hess has to take into consideration only the upper triangular portion + main diag.

jacIxConstr = np.zeros(n).tolist() #+ np.ones(n).tolist()
jacIxConstr = map(int, jacIxConstr)
jacIxVar = np.linspace(0, n-1, n).tolist() #+ np.linspace(0, n-1, n).tolist()
jacIxVar = map(int, jacIxVar)

hessCol = []
hessRow = []

for i in range(0, n):
    for j in range(0, n):
        if j>=i:
            hessCol.append(j)
            hessRow.append(i)

xInit = abs(np.random.randn(n)/n) #[ 9 ] * n
# Note: Solution sensitive to starting points. Infeasbile results obtained from startPoint = 1/n portfolio!
#xInit[n-1] = 1
# xInit = map(int, xInit)

#---- SETUP AND RUN KNITRO TO SOLVE THE PROBLEM.

#---- CREATE A NEW KNITRO SOLVER INSTANCE.
kc = KTR_new()
if kc == None:
    raise RuntimeError ("Failed to find a Knitro license.")

KTR_set_double_param_by_name(kc, "feastol", 1.0E-11)
#---- DEMONSTRATE HOW TO SET KNITRO PARAMETERS.
if KTR_set_char_param_by_name(kc, "outlev", "all"):
    raise RuntimeError ("Error setting parameter 'outlev'")
if KTR_set_int_param_by_name(kc, "hessopt", 1):
    raise RuntimeError ("Error setting parameter 'hessopt'")
if KTR_set_int_param_by_name(kc, "hessian_no_f", 1):
    raise RuntimeError ("Error setting parameter 'hessian_no_f'")
if KTR_set_double_param_by_name(kc, "feastol", 1.0E-15): # was 1.0E-10, 1.0E-15, np.finfo(float).eps
    raise RuntimeError ("Error setting parameter 'feastol'")

#------------------------------------------------------------------
#     FUNCTION callbackEvalFC
#------------------------------------------------------------------
 ## The signature of this function matches KTR_callback in knitro.h.
 #  Only "obj" and "c" are modified.
 ##
def callbackEvalFC (evalRequestCode, n, m, nnzJ, nnzH, x, lambda_, obj, c, objGrad, jac, hessian, hessVector, userParams):
    if evalRequestCode == KTR_RC_EVALFC:
        obj[0] = evaluateFC(x, c)
        return 0
    else:
        return KTR_RC_CALLBACK_ERR

#------------------------------------------------------------------
#     FUNCTION callbackEvalGA
#------------------------------------------------------------------
 ## The signature of this function matches KTR_callback in knitro.h.
 #  Only "objGrad" and "jac" are modified.
 ##
def callbackEvalGA (evalRequestCode, n, m, nnzJ, nnzH, x, lambda_, obj, c, objGrad, jac, hessian, hessVector, userParams):
    if evalRequestCode == KTR_RC_EVALGA:
        evaluateGA(x, objGrad, jac)
        return 0
    else:
        return KTR_RC_CALLBACK_ERR

#------------------------------------------------------------------
#     FUNCTION callbackEvalH
#------------------------------------------------------------------
 ## The signature of this function matches KTR_callback in knitro.h.
 #  Only "hessian" or "hessVector" is modified.
 ##
def callbackEvalH (evalRequestCode, n, m, nnzJ, nnzH, x, lambda_, obj, c, objGrad, jac, hessian, hessVector, userParams):
    if evalRequestCode == KTR_RC_EVALH:
        evaluateH(x, lambda_, 1.0, hessian)
        return 0
    elif evalRequestCode == KTR_RC_EVALH_NO_F:
        evaluateH(x, lambda_, 0.0, hessian)
        return 0
    else:
        return KTR_RC_CALLBACK_ERR

#---- REGISTER THE CALLBACK FUNCTIONS THAT PERFORM PROBLEM EVALUATION.
#---- THE HESSIAN CALLBACK ONLY NEEDS TO BE REGISTERED FOR SPECIFIC
#---- HESSIAN OPTIONS (E.G., IT IS NOT REGISTERED IF THE OPTION FOR
#---- BFGS HESSIAN APPROXIMATIONS IS SELECTED).
if KTR_set_func_callback(kc, callbackEvalFC):
    raise RuntimeError ("Error registering function callback.")
if KTR_set_grad_callback(kc, callbackEvalGA):
    raise RuntimeError ("Error registering gradient callback.")
if KTR_set_hess_callback(kc, callbackEvalH):
    raise RuntimeError ("Error registering hessian callback.")

#---- INITIALIZE KNITRO WITH THE PROBLEM DEFINITION.
ret = KTR_init_problem (kc, n, objGoal, objType, bndsLo, bndsUp,
                                cType, cBndsLo, cBndsUp,
                                jacIxVar, jacIxConstr,
                                hessRow, hessCol,
                                xInit, None)
if ret:
        raise RuntimeError ("Error initializing the problem, "
                            + "Knitro status = "
                            + np.str(ret))

#---- SOLVE THE PROBLEM.
#----
#---- RETURN STATUS CODES ARE DEFINED IN "knitro.h" AND DESCRIBED
#---- IN THE KNITRO MANUAL.
x       = [0] * n
lambda_ = [0] * (m + n)
obj     = [0]
nStatus = KTR_solve (kc, x, lambda_, 0, obj,
                         None, None, None, None, None, None)

#---- DISPLAY THE RESULTS.
print "Knitro finished, status %d: " % nStatus
if nStatus == KTR_RC_OPTIMAL_OR_SATISFACTORY:
    print "converged to optimality or satisfactory solution."
elif nStatus == KTR_RC_ITER_LIMIT:
    print "reached the maximum number of allowed iterations."
elif nStatus in [KTR_RC_NEAR_OPT, KTR_RC_FEAS_XTOL, KTR_RC_FEAS_FTOL, KTR_RC_FEAS_NO_IMPROVE]:
    print "could not improve upon the current iterate."
elif nStatus == KTR_RC_TIME_LIMIT:
    print "reached the maximum CPU time allowed."
else:
    print "failed."

#---- EXAMPLES OF OBTAINING SOLUTION INFORMATION.
print "  optimal value = %f" % obj[0]
print "  solution feasibility violation    = %f" % KTR_get_abs_feas_error(kc)
print "           KKT optimality violation = %f" % KTR_get_abs_opt_error(kc)
print "  number of function evaluations    = %d" % KTR_get_number_FC_evals(kc)

# post-processing
def rescaleWeights(solutionVec):
    normalFactor = sum(solutionVec)
    normalVector = np.asarray(solutionVec) * (1/normalFactor)
    return normalVector

def computeCorrMat(matSigma):
    n = matSigma.shape[0]
    matC = np.zeros((n, n))
    for i in range(0, n):
        for j in range(0, n):
            matC[i][j] = matSigma[i][j] / (matSigma[i][i] * matSigma[j][j])**(0.5)
    return matC

def computeVolaWeightedAvgCorr(scaledSolutionVector):
    # Prepare
    #filePath = "/Users/Dim/Desktop/work_folder/six/code_CPP/SIX/csv/"
    #fileName = "threeAssetTestPortfolio.csv"
    #matSigma = prepareProblem(filePath=filePath, shrinkage=True)
    matC = computeCorrMat(matSigma)
    n = matSigma.shape[0]
    vecVola = matSigma.diagonal()
    vecW = np.asarray(scaledSolutionVector)

    # Initialize sums
    top = 0
    bot = 0

    for i in range(0,n):
        for j in range(0,n):
            if(i != j):
                top += (vecVola[i]*vecW[i]*vecVola[j]*vecW[j]*matC[i][j])
                bot += (vecVola[i]*vecW[i]*vecVola[j]*vecW[j])

    return top/bot

def computeConcentrationRatio(scaledSolutionVector):
    # Prepare
    #filePath = "/Users/Dim/Desktop/work_folder/six/code_CPP/SIX/csv/"
    #fileName = "threeAssetTestPortfolio.csv"
    #matSigma = prepareProblem(filePath=filePath, shrinkage=True)
    n = matSigma.shape[0]
    vecVola = matSigma.diagonal()
    vecW = np.asarray(scaledSolutionVector)

    # Compute concentration ratio as per YC_YC_2011
    concentration = (np.dot(np.transpose([x**2 for x in vecW]), [x**2 for x in vecVola])) / (np.dot(np.transpose(vecW), vecVola))**2
    return concentration

def computeDiversificationRatio(solutionVec):
    # Prepare
    #filePath = "/Users/Dim/Desktop/work_folder/six/code_CPP/SIX/csv/"
    #fileName = "threeAssetTestPortfolio.csv"
    #matSigma = prepareProblem(filePath=filePath, shrinkage=True)
    n = matSigma.shape[0]
    vecVola = matSigma.diagonal()
    vecW = np.asarray(solutionVec)

    diversification = (np.dot(np.transpose(vecW), vecVola)) / (np.dot(np.dot(np.transpose(vecW), matSigma), vecW))
    return diversification


xRescaled = rescaleWeights(x)
concentration = computeConcentrationRatio(xRescaled)
volaWeightedAvgCorr = computeVolaWeightedAvgCorr(xRescaled)
diversification = computeDiversificationRatio(xRescaled)
print xRescaled
print "============="
print concentration
print "============="
print volaWeightedAvgCorr
print "============="
print diversification
print (volaWeightedAvgCorr * (1-concentration) + concentration)**(-1/2)

#---- BE CERTAIN THE NATIVE OBJECT INSTANCE IS DESTROYED.
KTR_free(kc)

#+++++++++++++++++++ End of source file +++++++++++++++++++++++++++++
