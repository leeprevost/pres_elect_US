from matplotlib.ticker import FuncFormatter, PercentFormatter

pct_formatter = PercentFormatter(1)
def millions(x, pos):
    'The two args are the value and tick position'
    return '%1.1fM' % (x * 1e-6)


formatter = FuncFormatter(millions)