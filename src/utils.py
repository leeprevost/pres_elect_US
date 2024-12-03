from matplotlib.ticker import FuncFormatter, PercentFormatter
from matplotlib import colormaps
import matplotlib.pyplot as plt
from functools import partial
from scipy.stats import zscore
from src import CACHE, DB
import os
import pandas as pd


cmap = colormaps["RdYlGn_r"]


zscore_all_cols = partial(zscore, axis=None, ddof=0)  # use ddof=0 if whole pop, 1 for just sample.
def millions(x, pos):
    'The two args are the value and tick position'
    return '%1.1fM' % (x * 1e-6)


millions_formatter = FuncFormatter(millions)
pct_formatter = PercentFormatter(1)


major_parties = ["DEMOCRAT", "REPUBLICAN"]
major_total = major_parties + ["TOTAL"]


# for caching
if not os.path.exists(DB):
    os.mkdir(DB)

db = CACHE
def get_key(key="seer", tfm = None, cache=True):

    def fetch_from_src():
        t = tfm()
        t.to_hdf(db, key=key)
        return t

    if cache:
        try:
            return pd.read_hdf(db, key=key)
        except Exception as e:
            print(e)
            print("Fetching from src")
            return fetch_from_src()

    else:
        return fetch_from_src()


def fix_fips(s):
    # zero padded two digit county followed by 3 digit zero padded county
    s = str(s)
    county = s[-3:]
    state = s[0:-3]
    return state.zfill(2) + county.zfill(3)

def footnote(ax, x=0.85, y=0.03, s='@leeprevost', **kwargs):
    return ax.figure.text(x, y, s, **kwargs)