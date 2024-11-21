import pandas as pd
import numpy as np
from sklearn.metrics import mean_absolute_error, mean_absolute_percentage_error
from src import vote_data
import utils
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.stats import zscore

# see docs/benford_citations.txt, using mae as error scorer.
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


mad_range = np.array([.004, .008, .012, np.inf])
mad_color = ['green', 'lightgreen', 'yellow', 'red']
mad_conform_label = ['High', 'Acceptable', "Marginal", "Non"]
def get_mad(val, color_only=False):
    i = np.searchsorted(mad_range, val)
    if color_only:
        return mad_color[i]
    else:
        return mad_conform_label[i], mad_color[i]



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

def benford_error(col, metric=mean_absolute_error):
    try:
        mae = metric(benford_range, digit_counts(col))

        return mae
    except:
        return np.nan


# shifting to mae - see docs/benford_citations.txt

pres_pt = vote_data.pres_pt
fips_key = vote_data.fips_key


benford_me = pres_pt.unstack(0).apply(benford_error).drop("MARGIN").sort_values(ascending=False)
benford_me.name = "benford_mean_absolute_error"

benford_raw = pres_pt.unstack(0).drop("MARGIN", axis=1).apply(digit_counts).assign(benford_expected=benford_range)
benford_raw_ae = benford_raw.sub(benford_raw.benford_expected, axis=0)
benford_raw_ae.name = 'benford ae'

def pct_error(col, expected = benford_range):
    return (col -expected)/expected

benford_raw_pe = benford_raw.transform(pct_error)
benford_raw_pe.name = 'benford pe'

ax = pd.concat([benford_raw_ae.mean(axis=1), benford_raw_pe.mean(axis=1)], axis=1).plot(kind='line')
ax.figure.show()

#benford_raw_pe = benford_raw.apply(pct_error)
benford_raw_ae_zscore = benford_raw_ae.transform(utils.zscore_all_cols)
anomaly_col = (benford_raw_ae_zscore > 2).any()
benford_raw_ae_anomaly_years = benford_raw.drop(["benford_expected"], axis=1).loc[:, anomaly_col]
anomaly_mask = (benford_raw_ae_zscore > 2)[benford_raw_ae_anomaly_years.columns]

def pretty_table(styler):

    cell_hover = {  # for row hover use <tr> instead of <td>
        'selector': 'td:hover',
        'props': [('background-color', '#ffffb3')]
    }
    index_names = {
        'selector': '.index_name',
        'props': 'font-style: italic; color: darkgrey; font-weight:normal;'
    }
    headers = {
        'selector': 'th:not(.index_name)',
        'props': 'background-color: #000066; color: white;'
    }
    styler.set_table_styles([cell_hover, index_names, headers])
    styler.set_caption("Benford Anomalies 2000-2020")
    styler.background_gradient(cmap=utils.cmap, axis=None)
    styler.format_index('{:.1f}')
    styler.format('{:.2%}')
    return styler

benford_raw_ae.loc[:, anomaly_col].abs().style.pipe(pretty_table).to_html("../tabs/benford_anomaly.html")
# prob better to filter down to major parties, totals here.

def highlight_mask(s):
    return ['color: red' if v else '' for v in s]

benford_raw_ae_anomaly_years.to_excel("../tabs/benford_anomalous_years.xlsx")


ax = benford_me.dropna().sort_values().plot(kind='barh')
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

benford_data = benford_range.copy().reset_index(drop=True)
benford_data.name = 'frequency'
p_data = benford_raw.drop(["benford_expected", "OTHER", "LIBERTARIAN", "GREEN"], axis=1).melt(ignore_index=False).reset_index().rename(columns = {"value": "frequency"})
g = sns.FacetGrid(p_data, col="party",  row="year")
g.map_dataframe(sns.barplot, y="frequency", x='digits')
g.despine(left=True)
g.tight_layout()
for ax in g.figure.get_axes():

    benford_data.plot(kind='line', ax=ax)
    ax.yaxis.set_major_formatter(utils.pct_formatter)
    mae = f"mae = {benford_me.xs(get_party_yr(ax)):.2%}"
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
benford_2020 = benford_raw.xs(2020, level=1, axis=1).join(benford_range)
benford_DEM_2020_error = (benford_2020.DEMOCRAT - benford_range)
benford_ae_DEM_2020 = benford_raw_ae['DEMOCRAT'][2020].sort_values()
benford_ae_zscores = benford_raw_ae.transform(utils.zscore_all_cols).abs()
benford_ae_zscores_2020 = benford_ae_zscores.xs(2020, level=1, axis=1)

anomalous_zscores_2020 = benford_ae_zscores_2020 > 1.5


ax  = benford_DEM_2020_error.plot(kind='barh')
ax.figure.suptitle("Benford's Law Error Democrat Vote 2020")
ax.set_title("@leeprevost, source: Harvard Dataverse, 11/18/2024")
ax.figure.savefig("../img/benford_dem_2020_pe.jpg")
ax.figure.show()
# on major parties and totals, these include DEMs shifting to digit 4 (also from 5) from prev, Green shifting to 1, REPs shifting to 2, and Total shift to 3

benford_ae_zscore_DEM_2020 = benford_ae_zscores["DEMOCRAT"][2020]
digit_shift_data= pres_pt.unstack(0).transform(digit_shift)
digit_shift_data.drop("MARGIN", axis=1, inplace=True)
digit_shift_data = digit_shift_data.transform(pair_cols_combine)
digit_shift_DEM_2020 = digit_shift_data["DEMOCRAT"][2020]

def filt_shift(s, culprit_digits = (3,4)):
    prev, curr = s
    if prev==curr:
        return False
    elif curr in culprit_digits:
        return True
    else:
        return False

def filt_shift_fr_to(s, from_to = (5, 4)):
    prev, curr = s
    fr, to = from_to
    if prev==curr:
        return False
    elif prev == fr:
        return True
    elif curr == to:
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
# theory -- odd shifts are those tht shift more than 2 digits.  Also where the change from 16-20 is anomalous vs. pop.
# zscore of 2 and being on two lists mean probability of occurrence is 2% * 2% or .0004 or .04%

desc, colname, votes_in_question, fips_ct, fips_sum = anomalous_sum[0]
mask_45 = digit_shift_DEM_2020.apply(filt_shift, culprit_digits=(4,5)) #casts wider net and could include double jumps or odd jumps
mask_5_to_4 = digit_shift_DEM_2020.apply(filt_shift_fr_to, from_to=(5,4))   # includes those that shifted from 5 in 2016
anomalous_votes = pres_pt.loc[[2016,2020]].unstack(0).loc[mask_45]["DEMOCRAT"]
anomalous_votes = anomalous_votes.join(fips_key).reset_index()
anomalous_votes = anomalous_votes.assign(fips_fixed = anomalous_votes.county_fips.apply(vote_data.fix_fips))
anomalous_votes = anomalous_votes.set_index("fips_fixed", drop=True).drop("POP_ESTIMATE_2020", axis=1).join(vote_data.pop_est_2020.POP_ESTIMATE_2020)
anomalous_votes = anomalous_votes.assign(vote_diff_pct_pop = (anomalous_votes[2020]-anomalous_votes[2016])/anomalous_votes.POP_ESTIMATE_2020)
anomalous_votes = anomalous_votes.assign(vote_diff_pct_pop_zscore = zscore(anomalous_votes.vote_diff_pct_pop.dropna()))
# Ok, am seeing some wild shift.  Zscores as high at 5 for vote margins over population!  Need to go back and do pop analysis on full dataset then come back to this.

