from dataPreProcess import *
import numpy as np
import pandas as pd

# Set the path and filename of the historical data to be used
filePath = "/Users/Dim/Desktop/school_folder/masters_thesis/gitCodeRepo/data/"
fileName = "historicalData_fill_20160809.csv"

# Read .csv file, prepare an appropriate subset of the data, calculate variance-covariance matrix
dictData = prepareData(filePath, fileName)
tsData   = fetchDataSubset(dictData['data'], dictData['tfdata'], dictData['date'], lookbackLength = 0)['data']
tsDate   = fetchDataSubset(dictData['data'], dictData['tfdata'], dictData['date'], lookbackLength = 0)['date']
Sigma    = prepareSigma(tsData)

# Align df's to common date based index
tsData = pd.concat([tsData, tsDate], axis=1)
tsData = tsData.set_index('date')

# Adjust "MXHK Index ISIN": index is in HKD, equity is in USD
hkIndex_HKD = pd.to_numeric(tsData['MXHK Index ISIN'])
crcyHKDUSD  = pd.to_numeric(tsData['HKDUSD BGN Curncy ISIN'])

# Apply CCY conversion
hkIndex_USD = np.multiply(hkIndex_HKD, crcyHKDUSD)
hkIndex_USD.rename("MXHK (USD) Index ISIN")
tsData = pd.concat([tsData, hkIndex_USD], axis=1)



