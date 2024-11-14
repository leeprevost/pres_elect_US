import pandas as pd
import numpy as np
from sklearn.metrics import mean_absolute_error

def digit_counts(col):
    # clean - dropna, convert to clean integers, make absolute value, drop decimals and leading zeroes
    col = col.dropna().convert_dtypes(convert_integer=True).abs().astype(str)
    col = col.str.replace("\.", "", regex=True).replace("^0+", "", regex=True)  # drops decimals
    ct = col.str[0].astype(float).value_counts()
    total = ct.sum()
    dist = ct/total
    dist.name = col.name
    dist.index.name = "digits"
    return dist

def benford(n):
    return np.log10(1 + 1/n)

ndx = pd.Index(range(1,10))
benford_range = pd.Series([benford(n) for n in ndx], index=ndx, name = 'benford')

def benford_error(col, metric=mean_absolute_error):
    try:
        mae = metric(digit_counts(col), benford_range)

        return mae
    except:
        return np.nan



