import pandas as pd
import numpy as np
import re

# function prepareData
# @param fileName
# @param lookbackLength is the window size (of observations) that should be extracted from the historical time-series
def prepareData(filePath, fileName):
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
    dateList = list()
    counter = 0

    # Loops through the header vect. and extracts the names. Comparable with metaData_YYYYMMDD::BBG_ISIN
    for item in colList:
        match = re.search(pattern=r"(ISIN)$", string=item)
        if match:
            tickerList.append(item)

    for item in colAttributeList:
        match2 = re.search(pattern=r"(PX_LAST){1}", string=item)
        counter += 1
        if match2:
            attributeList.append(counter)

    for item in attributeList:
        colList2.append(colList[item - 1])

    dateList.append(min(attributeList)-2)
    date = df[dateList]
    data = df[colList2]
    tfdata = trueFalseDF[colList2]
    data = data.drop(data.index[[0,0]])
    date = date.drop(date.index[[0,0]])
    tfdata = tfdata.drop(tfdata.index[[0,0]])
    data.columns = tickerList
    tfdata.columns = tickerList
    date.columns = ["date"]

    return {"data": data, "tfdata": tfdata, "date": date}


def fetchDataSubset(data, tfdata, date, lookbackLength = 0):
    # Check the rows for the longest possible set of time-series
    rowCheck = min(min(np.where(tfdata.sum(1) == 0)))
    T = tfdata.__len__()
    maxIndex = T - rowCheck

    if lookbackLength > maxIndex:
        lookbackLength = maxIndex

    if lookbackLength == 0:
        lookbackLength = maxIndex

    dataStartIndex = T - lookbackLength
    data   = data[int(dataStartIndex):int(T)]
    tfdata = tfdata[int(dataStartIndex):int(T)]
    date   = date[int(dataStartIndex):int(T)]

    return {"data": data, "tfdata": tfdata, "date": date}

# Function prepareSigma
# @param data: a pandas data-frame consisting of numeric time-series, expects no date series
def prepareSigma(data):
    # variance-covariance matrix (numpy-array)
    data = data.apply(pd.to_numeric)
    Sigma = (data.cov()).as_matrix()

    return Sigma




