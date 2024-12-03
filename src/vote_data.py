import pandas as pd
import numpy as np

from src import census
from utils import fix_fips
import src
pres_history = r"C:\Users\lee\Downloads\countypres_2000-2020.csv"

cite = "https://dataverse.harvard.edu/dataset.xhtml?persistentId=doi:10.7910/DVN/VOQCHQ"

pop_est_2020 = census.pop_est_2020


pres = pd.read_csv(pres_history, dtype={'county_fips': str})



#pres['county_fips'] = pres.county_fips.apply(fix_fips)
#prob_fips = pres.loc[pres.county_fips.apply(len) == 7]

# in spite of this, all of Kansas City, MO is in one 7 digit fips, not sure what to do with those.
# left it in although this won't line up with pop data.

fips_key = pres.groupby("county_fips").last()[['state', "state_po", "county_name"]]
fips_key_2_index = pd.MultiIndex.from_product((["demographics"], fips_key.columns))
fips_key['fixed_fips'] = fips_key.reset_index().county_fips.apply(fix_fips).values
fips_key = pd.merge(pop_est_2020.POP_ESTIMATE_2020, fips_key, right_on='fixed_fips', left_index=True)
def log_bins(data, num_bins):
    data = data.dropna()
    log_min = np.log10(min(data))
    log_max = np.log10(max(data))
    bins = np.logspace(log_min, log_max, num_bins+1)
    return bins


pres_pt = pres.pivot_table(index = ["year", "county_fips"], columns = "party", values = 'candidatevotes', aggfunc='sum')

major_parties = ["DEMOCRAT", "REPUBLICAN"]
major_total = major_parties + ["TOTAL"]

total_cts = pres_pt[['DEMOCRAT', "REPUBLICAN"]].unstack(0).sum().unstack(0)

pres_pt = pres_pt.assign(TOTAL = pres_pt.sum(axis=1))
pres_pt = pres_pt.assign(MARGIN = (pres_pt.REPUBLICAN - pres_pt.DEMOCRAT)/pres_pt.TOTAL)
pres_pt.to_csv("pres_pt.csv")


rec_total_votes = pres_pt.loc[[2016, 2020], "TOTAL"].unstack(0).max(axis=1).replace(0.0, np.nan)
rec_total_votes.name = 'size'
l_b = log_bins(rec_total_votes, 5)

tot_votes = rec_total_votes.sum()
tot_votes_bin = tot_votes // 5
cum_sum = rec_total_votes.sort_values().cumsum()
eq_vote_cuts = sorted(rec_total_votes.loc[((cum_sum % tot_votes_bin).pct_change(fill_method=None) < 0)].sort_values().to_list() + [0])

labels = ['xs', 's', 'm', "l", 'xl']
fips_key = fips_key.join(pd.cut(rec_total_votes, bins = eq_vote_cuts, labels = ['xs', 's', 'm', 'l', 'xl'])).rename(columns = {'totvotes': "size"})

fips_key.to_hdf(src.CACHE, key = 'fips_key', format='table')