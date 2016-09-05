# coding=utf-8

from datetime import datetime
import pandas as pd
import matplotlib.pyplot as plt

def getRollingCovariance(filePath, winSize):
    # Import data from .csv
    df = pd.read_csv(filePath, sep=';')
    df.index = df.date
    df = df.drop('date', axis=1)

    # Prototype for datetime conversion
    # date_obj = datetime.strptime(df.index.values, '%d.%m.%Y')

    # Implement datetime conversion
    bucket = []
    for item in df.index.values:
        bucket.append(datetime.strptime(item, '%d.%m.%Y').isoformat(sep='.'))

    dateIndex = bucket
    df.index = dateIndex
    del bucket

    return {'rollCov':df.rolling(window=winSize).cov(df, pairwise=True), 'df':df}

#r.loc[:, 'HK0000069689 Equity ISIN', 'US0231351067 Equity ISIN'].plot(figsize=(8,8), rot=90); plt.show()

# Select rolling covariance matrices
#s = r[df.index[range(60,2239,60)]]

#df.index[range(120,2239,60)]
#s['2008-06-18.00:00:00']