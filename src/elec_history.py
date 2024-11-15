import pandas as pd
import numpy as np
from matplotlib.ticker import FuncFormatter, PercentFormatter
import matplotlib.pyplot as plt
import requests
from scipy.stats import zscore
from src.benford import benford_error, digit_counts, benford_range, digit_shift, pair_cols_combine
import seaborn as sns


#date source: https://dataverse.harvard.edu/dataset.xhtml?persistentId=doi:10.7910/DVN/VOQCHQ
# direct link may be:  https://dataverse.harvard.edu/dataset.xhtml?persistentId=doi:10.7910/DVN/VOQCHQ# but requires accepting terms

pres_history = r"C:\Users\lee\Downloads\countypres_2000-2020.csv"
pop_est_2020_url = "https://www.ers.usda.gov/webdocs/DataFiles/48747/PopulationEstimates.xlsx?v=9655.3"

pop_est_2020 = pd.read_excel(pop_est_2020_url, skiprows=4, dtype={'FIPStxt': str}).rename(columns={"FIPStxt": 'county_fips'}).set_index('county_fips', drop=True)
#good source for 2024 reporting of state and county level results.
nyt_api = "https://static01.nyt.com/elections-assets/2020/data/api/2020-11-03/national-map-page/national/president.json"


r = requests.get(nyt_api)
nyt = r.json()


pres = pd.read_csv(pres_history, dtype={'county_fips': str})

def fix_fips(s):
    # zero padded two digit county followed by 3 digit zero padded county
    s = str(s)
    county = s[-3:]
    state = s[0:-3]
    return state.zfill(2) + county.zfill(3)

#pres['county_fips'] = pres.county_fips.apply(fix_fips)
#prob_fips = pres.loc[pres.county_fips.apply(len) == 7]

# in spite of this, all of Kansas City, MO is in one 7 digit fips, not sure what to do with those.
# left it in although this won't line up with pop data.

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
ax.figure.savefig("../img/us_pop_vote.jpg")

pres_pt = pres_pt.assign(TOTAL = pres_pt.sum(axis=1))
pres_pt = pres_pt.assign(MARGIN = (pres_pt.REPUBLICAN - pres_pt.DEMOCRAT)/pres_pt.TOTAL)
pres_pt.to_csv("pres_pt.csv")

rec_total_votes = pres_pt.loc[[2016, 2020], "TOTAL"].unstack(0).max(axis=1).replace(0.0, np.nan)
rec_total_votes.name = 'size'
l_b = log_bins(rec_total_votes, 5)

tot_votes = rec_total_votes.sum()
tot_votes_bin = tot_votes // 5
cum_sum = rec_total_votes.sort_values().cumsum()
eq_vote_cuts = sorted(rec_total_votes.loc[((cum_sum % tot_votes_bin).pct_change() < 0)].sort_values().to_list() + [0])

labels = ['xs', 's', 'm', "l", 'xl']
fips_key = fips_key.join(pd.cut(rec_total_votes, bins = eq_vote_cuts, labels = ['xs', 's', 'm', 'l', 'xl'])).rename(columns = {'totvotes': "size"})


democrat_over_time = pres_pt['DEMOCRAT'].unstack(0).join(fips_key).set_index(list(fips_key.columns), append = True)
democrat_20_16_pct_change = democrat_over_time.pct_change(axis=1)[2020]
democrat_20_16_pct_change.name = "pct_change"
democrat_20_16_diff = democrat_over_time.diff(axis=1)[2020]
democrat_20_16_diff.name = "vote_change"
stats_00_16_pct_change = democrat_over_time.iloc[:, 0:-1].pct_change(axis=1).agg(['std', 'median'], axis=1)

diff_16_20 = pd.concat([democrat_20_16_pct_change, democrat_20_16_diff], axis = 1)

diff_16_20 = pd.concat({'2000_2016_pct_chg' : stats_00_16_pct_change, "2016_2020": diff_16_20}, axis=1)
diff_16_20.to_csv("../tabs/diff_16_20.csv")

top_shift_16_20 =diff_16_20.iloc[:, -1].sort_values().nlargest(30)
top_shift_16_20 = top_shift_16_20.reset_index(level=(0,1,4), drop = True).swaplevel().sort_values(ascending=True)
top_shift_16_20.index = pd.MultiIndex.from_tuples(top_shift_16_20.index)
total = top_shift_16_20.sum()
format_total = "{:.2f}M".format(total / 1000000)
ax = top_shift_16_20.plot(kind='barh', figsize= (15,20), title = "@leeprevost, source: Harvard Dataverse, 11/8/24")
ax.figure.suptitle(f"Where Did Additional {format_total} Biden Votes Come From Over 2016?", size='xx-large')

ax.figure.show()
ax.figure.savefig("../img/inc_20_demo_votes.jpg")

democrat_20_16_pct_change.to_csv("../tabs/democrat_2016_2020_pct_change.csv")
margin_over_time = pres_pt.unstack(0)["MARGIN"].join(fips_key).set_index(list(fips_key.columns), append=True)
margin_over_time.to_csv("../tabs/margin_shift_over_time.csv")

margin_shift = margin_over_time.diff(axis=1)

margin_shift_20 = margin_shift[2020].to_frame().join(fips_key).sort_values(2020).set_index('size', append=True).swaplevel().sort_index().set_index(["state_po", 'county_name'], append=True).drop('state', axis=1)
margin_shift_20.to_csv("../tabs/margin_shift_20.csv")



# finding outliers in 2020 election
# need to fill margin for about 6 counties that have NaN values.   Fill with median for year
year_medians = margin_over_time.median()
margin_over_time.fillna(year_medians, inplace=True)

# now perform zscore on entire dataset (axis=None)
margin_zscores = zscore(margin_over_time.values, axis=None)

# now id outliers defined as zscore > 2 (pos or neg)
outlier_mask = abs(margin_zscores[:, -1]) > 2
outliers = margin_over_time.loc[outlier_mask]
outliers.to_csv("../tabs/outliers_2020_vote.csv")

# plot histogram of margins over time
margin_over_time.hist(log=True, figsize = (12, 15))
plt.suptitle("Distribution of Vote Margins By County\n(negative = D, positive = R)\n@leeprevost, source=Harvard Dataverse")
plt.savefig("../img/distribution_vote_margins_county.jpg")
plt.show()

# now do benford law calcs
benford_mae = pres_pt.unstack(0).apply(benford_error).drop("MARGIN").sort_values(ascending=False)
benford_mae.name = "benford_mean_absolute_error"

benford_raw = pres_pt.unstack(0).apply(digit_counts).assign(benford_expected=benford_range)
benford_raw_ae = benford_raw.iloc[:, 0:-1].sub(benford_raw.benford_expected, axis=0).abs()
benford_raw.to_csv("../tabs/benford_raw.csv")


ax = benford_mae.dropna().sort_values().plot(kind='barh')
plt.suptitle("Benford's Law US Presidential Elections (2000-2020)")
plt.title("@leeprevost, source data: Harvard Dataverse, 11/12/2024", size='x-small')
plt.tight_layout(pad=1.4)
ax.set_xlabel("Mean Absolute Error")
#plt.xticks(rotation=90, ha='right')
plt.savefig("../img/benford_us_ele.jpg")
ax.figure.show()

plt.clf()
worst_broad_error = benford_raw["DEMOCRAT"][2004]
worst_broad_error.name = "DEMOCRAT, 2004"
worst_broad_error.index = pd.Index(range(1,10))
benford_range.name = "Benford Expected"
ax = worst_broad_error.plot(kind='bar')
benford_range.reset_index().plot(kind='line', ax=ax)
ax.set_ylim((0, .35))
ax.legend(labels = ["DEMOCRAT, 2004", "Benford Expected"])
plt.suptitle("Benford Analysis on 'Worst' Broad Election Error (2000 - 2020)")
plt.title("@leeprevost, source data: Harvard Dataverse, date: 11/12/2024",size = 'x-small')
plt.savefig("../img/benford_error_worst.jpg")
ax.figure.show()


def get_party_yr(ax):
    text = ax.title._text
    sp = text.split(" = ")
    party = sp[-1]
    yr = "".join((ch for ch in sp[1] if ch.isnumeric()))
    return party, int(yr)

pct_formatter = PercentFormatter(1)
benford_data = benford_range.copy().reset_index(drop=True)
benford_data.name = 'frequency'
p_data = benford_raw.drop(["MARGIN","benford_expected", "OTHER", "LIBERTARIAN", "GREEN"], axis=1).melt(ignore_index=False).reset_index().rename(columns = {"value": "frequency"})
g = sns.FacetGrid(p_data, col="party",  row="year")
g.map_dataframe(sns.barplot, y="frequency", x='digits')
g.despine(left=True)
g.tight_layout()
for ax in g.figure.get_axes():

    benford_data.plot(kind='line', ax=ax)
    ax.yaxis.set_major_formatter(pct_formatter)
    mae = f"mae = {benford_mae.xs(get_party_yr(ax)):.2%}"
    if mae:
        ax.text(*(3, .20), s=mae)

title = """
Benford's Law on US Presidential Elections 2000-2020 County Level"""
subtitle = "@leeprevost, source_data: Harvard Dataverse, 11/14/2024"

g.figure.subplots_adjust(top=0.9, bottom=0.05) # adjust the Figure in rp
g.figure.suptitle(title)
plt.figtext(0.5, 0.01, subtitle, ha="center", fontsize=10)
g.savefig("../img/benford_facet.jpg")

g.figure.show()


# now seeing an anomaly -- seeing some odd things in Benford charts for 2020, Democrats.  Drilling down

benford_ae_DEM_2020 = benford_raw_ae['DEMOCRAT'][2020].sort_values()
benford_ae_zscores = benford_raw_ae.drop("MARGIN" , axis=1).transform(lambda df: abs(zscore(df, axis=None)))
benford_ae_zscores_2020 = benford_ae_zscores.xs(2020, level=1, axis=1)
anomalous_zscores_2020 = benford_ae_zscores_2020 > 1.5

# on major parties and totals, these include DEMs shifting to digit 4 from prev, Green shifting to 1, REPs shifting to 2, and Total shift to 3
# question: focus on Total as this is observed?  But so are others.

benford_ae_zscore_DEM_2020 = benford_ae_zscores["DEMOCRAT"][2020]
digit_shift = pres_pt.unstack(0).transform(digit_shift)
digit_shift.drop("MARGIN", axis=1, inplace=True)
digit_shift = digit_shift.transform(pair_cols_combine)
digit_shift_DEM_2020 = digit_shift["DEMOCRAT"][2020]

def filt_shift(s, culprit_digits = (3,4)):
    prev, curr = s
    if prev==curr:
        return False
    elif curr in culprit_digits:
        return True
    else:
        return False

# rules compiled from zscores > 1.5 from anomalous_zscores_2020
anomalies_2020_inputs = [
    ("DEM Shift to Digit 4", "DEMOCRAT", "D4", 4),
    ("GREEN Shift to 1", "GREEN", "G1", 1),
    ("REP Shift to Digit 2", "REPUBLICAN", 'R2', 2),
    ("Total Shift to Digit 3", "TOTAL", "T3", 3)
]

anomalous_sum = []
for anomaly_tup in anomalies_2020_inputs:
    desc, filt_key, colname, digit = anomaly_tup
    mask = digit_shift_DEM_2020.apply(filt_shift, culprit_digits=(digit,))
    votes_in_question = pres_pt[filt_key][2020].loc[mask].sum()
    fips_sum = fips_key.groupby(["state", 'size'], observed=False)['county_name'].count().unstack(1)
    fips_ct = mask.sum()
    anomalous_sum.append((desc, colname, votes_in_question, fips_ct, fips_sum))

anomalous_sum_print = pd.DataFrame((tup[0:-1] for tup in anomalous_sum ))

# again, going back to my core question, where did Biden votes come from?  Focus on group D4 for now, acknowledging there are other questions.

desc, colname, votes_in_question, fips_ct, fips_sum = anomalous_sum[0]
mask = digit_shift_DEM_2020.apply(filt_shift, culprit_digits=(4,))
