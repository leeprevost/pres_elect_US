import pandas as pd
import numpy as np
from sklearn.metrics import mean_absolute_error, mean_absolute_percentage_error
from itertools import pairwise

def first_digit_cleaned(col):
    # clean - dropna, convert to clean integers, make absolute value, drop decimals and leading zeroes
    col = col.dropna().convert_dtypes(convert_integer=True).abs().astype(str)
    col = col.str.replace("\.", "", regex=True).replace("^0+", "", regex=True)  # drops decimals
    return col.str[0].astype(float)

def digit_shift(df, periods=1, axis=0):
    if axis==1:
        df = df.T
    digit = df.apply(first_digit_cleaned)
    digit_shift = digit.shift(periods=periods, axis= 1 )
    return digit.compare(digit_shift, align_axis=1, keep_shape=True, keep_equal=True, result_names = ("current", "previous"))


def pair_cols_combine(df, level=(0,1)):
    """use this with transform to put shift columns into a single tup col"""
    df = df.T
    g = df.groupby(level=level)
    cols = []
    for ndx, f in g:
        curr, prev = f.index
        curr_level = len(curr)
        list_of_tups = list(map(tuple, f.T.values.tolist()))
        list_of_tups = [tuple((pre, self)) for self, pre in list_of_tups]
        new_col  = pd.Series(list_of_tups, index=f.columns, name=curr[0:-(curr_level -len(level))])
        cols.append(new_col)
    return pd.concat(cols, axis=1)






def digit_counts(col):
    ct = first_digit_cleaned(col).value_counts()
    total = ct.sum()
    dist = ct/total
    dist.name = col.name
    dist.index.name = "digits"
    return dist

def benford(n):
    return np.log10(1 + 1/n)

ndx = pd.Index(range(1,10))
benford_range = pd.Series([benford(n) for n in ndx], index=ndx, name = 'benford')

def benford_error(col, metric=mean_absolute_percentage_error):
    try:
        mae = metric(benford_range, digit_counts(col))

        return mae
    except:
        return np.nan



