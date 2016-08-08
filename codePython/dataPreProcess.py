import pandas as pd
import numpy as np
import re

# function prepareProblem: this function constructs the variance-covariance matrix
# @param filePath
# @param fileName
def prepareProblem(filePath, fileName, lookbackLength = 0):
    # read data, eliminate NaN's
    df = pd.read_csv(filePath + fileName, sep = ";")
    trueFalseDF = df.isnull()
    df = df.fillna(value='#VALUE')

    # match items in colList that are tickers & attributes
    colList = list(df.columns.values) # tickers
    colList2 = list() # attributes
    colAttributeList = map(list, df.values[:1])
    colAttributeList = [item for sublist in colAttributeList for item in sublist]
    tickerList = list()
    attributeList = list()
    counter = 0

    # Loops through the header vect. and extracts the names. Comparable with metaData_YYYYMMDD::BBG_ISIN
    for item in colList:
        match = re.search(pattern=r".{12}\s(Equity ISIN){1}", string=item)
        if match:
            tickerList.append(item)

    for item in colAttributeList:
        match2 = re.search(pattern=r"(PX_LAST){1}", string=item)
        counter += 1
        if match2:
            attributeList.append(counter)

    for item in attributeList:
        colList2.append(colList[item - 1])

    data = df[colList2]
    tfdata = trueFalseDF[colList2]
    data = data.drop(data.index[[0,0]])
    tfdata = tfdata.drop(tfdata.index[[0,0]])
    data.columns = tickerList
    tfdata.columns = tickerList

    # Check the rows for the longest possible set of time-series
    rowCheck = min(min(np.where(tfdata.sum(1) == 0)))
    T = tfdata.__len__()
    maxIndex = T - rowCheck

    if(lookbackLength > maxIndex):
        lookbackLength = maxIndex

    dataStartIndex = T - lookbackLength
    data = data[int(dataStartIndex):int(T)]

    # variance-covariance matrix (numpy-array)
    data = data.apply(pd.to_numeric)
    Sigma = (data.cov()).as_matrix()

    return Sigma


filePath = "/Users/Dim/Desktop/school_folder/masters_thesis/gitCodeRepo/data/"
fileName = "historicalData_20160808.csv"

testdf = prepareProblem(filePath, fileName)