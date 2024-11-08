import pandas as pd
import numpy as np
from matplotlib.ticker import FuncFormatter
import matplotlib.pyplot as plt
import requests
from scipy.stats import zscore


#date source: https://dataverse.harvard.edu/dataset.xhtml?persistentId=doi:10.7910/DVN/VOQCHQ
pres_history = r"C:\Users\lee\Downloads\countypres_2000-2020.csv"


#good source for 2024 reporting of state and county level results.
nyt_api = "https://static01.nyt.com/elections-assets/2020/data/api/2020-11-03/national-map-page/national/president.json"


r = requests.get(nyt_api)
nyt = r.json()

pres = pd.read_csv(pres_history)

fips_key = pres.groupby("county_fips").last()[['state', "state_po", "county_name"]]

def log_bins(data, num_bins):
    data = data.dropna()
    log_min = np.log10(min(data))
    log_max = np.log10(max(data))
    bins = np.logspace(log_min, log_max, num_bins+1)
    return bins


def millions(x, pos):
    'The two args are the value and tick position'
    return '%1.1fM' % (x * 1e-6)


formatter = FuncFormatter(millions)

pres_pt = pres.pivot_table(index = ["year", "county_fips"], columns = "party", values = 'candidatevotes', aggfunc='sum')

total_cts = pres_pt[['DEMOCRAT', "REPUBLICAN"]].unstack(0).sum().unstack(0)
ax = total_cts.iloc[3:, :].plot(kind='bar', color=['blue', 'red'], title = "US Presidential Election Popular Vote: Democrat vs. Republican (millions)\n@leeprevost, 11/8/2024")
ax.yaxis.set_major_formatter(formatter)
ax.legend(loc='upper center', bbox_to_anchor=(0.4, 1.00),
          ncol=3, )
ax.figure.show()
ax.figure.savefig("us_pop_vote.jpg")

pres_pt = pres_pt.assign(TOTAL = pres_pt.sum(axis=1))
pres_pt = pres_pt.assign(MARGIN = (pres_pt.REPUBLICAN - pres_pt.DEMOCRAT)/pres_pt.TOTAL)
pres_pt.to_csv("pres_pt.csv")

rec_total_votes = pres_pt.loc[[2016, 2020], "TOTAL"].unstack(0).max(axis=1).replace(0.0, np.nan)
rec_total_votes.name = 'size'
l_b = log_bins(rec_total_votes, 5)

fips_key = fips_key.join(pd.cut(rec_total_votes, bins = l_b, labels = ['xs', 's', 'm', 'l', 'xl']))

democrat_over_time = pres_pt['DEMOCRAT'].unstack(0).join(fips_key).set_index(list(fips_key.columns), append = True)
democrat_20_16_pct_change = democrat_over_time.pct_change(axis=1)[2020]
democrat_20_16_pct_change.name = "pct_change"
democrat_20_16_diff = democrat_over_time.diff(axis=1)[2020]
democrat_20_16_diff.name = "vote_change"
stats_00_16_pct_change = democrat_over_time.iloc[:, 0:-1].pct_change(axis=1).agg(['std', 'median'], axis=1)

diff_16_20 = pd.concat([democrat_20_16_pct_change, democrat_20_16_diff], axis = 1)

diff_16_20 = pd.concat({'2000_2016_pct_chg' : stats_00_16_pct_change, "2016_2020": diff_16_20}, axis=1)

top_shift_16_20 =diff_16_20.iloc[:, -1].sort_values().nlargest(30)
top_shift_16_20 = top_shift_16_20.reset_index(level=(0,1,4), drop = True).swaplevel().sort_values(ascending=True)
top_shift_16_20.index = pd.MultiIndex.from_tuples(top_shift_16_20.index)
total = top_shift_16_20.sum()
format_total = "{:.2f}M".format(total / 1000000)
ax = top_shift_16_20.plot(kind='barh', figsize= (15,20), title = "@leeprevost, source: Harvard Dataverse, 11/8/24")
ax.figure.suptitle(f"Where Did Additional {format_total} Biden Votes Come From Since 2016?", size='xx-large')

ax.figure.show()
ax.figure.savefig("inc_20_demo_votes.jpg")

democrat_20_16_pct_change.to_csv("democrat_2016_2020_pct_change.csv")
margin_over_time = pres_pt.unstack(0)["MARGIN"].join(fips_key).set_index(list(fips_key.columns), append=True)
margin_over_time.to_csv("margin_shift_over_time.csv")

margin_shift = margin_over_time.diff(axis=1)

margin_shift_20 = margin_shift[2020].to_frame().join(fips_key).sort_values(2020).set_index('size', append=True).swaplevel().sort_index().set_index(["state_po", 'county_name'], append=True).drop('state', axis=1)
margin_shift_20.to_csv("margin_shift_20.csv")