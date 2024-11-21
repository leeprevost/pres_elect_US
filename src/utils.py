from matplotlib.ticker import FuncFormatter, PercentFormatter
from matplotlib import colormaps
import matplotlib.pyplot as plt
from functools import partial
from scipy.stats import zscore


cmap = colormaps["RdYlGn_r"]


zscore_all_cols = partial(zscore, axis=None, ddof=0)  # use ddof=0 if whole pop, 1 for just sample.
def millions(x, pos):
    'The two args are the value and tick position'
    return '%1.1fM' % (x * 1e-6)


millions_formatter = FuncFormatter(millions)
pct_formatter = PercentFormatter(1)


major_parties = ["DEMOCRAT", "REPUBLICAN"]
major_total = major_parties + ["TOTAL"]