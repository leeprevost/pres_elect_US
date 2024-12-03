import pandas as pd
import numpy as np

import matplotlib.pyplot as plt
from scipy.stats import zscore
import seaborn as sns

#sklearn
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import Normalizer, PowerTransformer
from sklearn.pipeline import Pipeline
from sklearn.ensemble import IsolationForest
from sklearn.svm import OneClassSVM
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
import utils

from src import vote_data
from src import benford

pres_pt = vote_data.pres_pt
fips_key = vote_data.fips_key





total_cts = pres_pt[['DEMOCRAT', "REPUBLICAN"]].unstack(0).sum().unstack(0)
ax = total_cts.iloc[3:, :].plot(kind='bar', color=['blue', 'red'], title = "US Presidential Election Popular Vote: Democrat vs. Republican (millions)\n@leeprevost, 11/8/2024")
ax.yaxis.set_major_formatter(utils.millions_formatter)
ax.legend(loc='upper center', bbox_to_anchor=(0.4, 1.00),
          ncol=3, )
ax.figure.show()
ax.figure.savefig("../img/us_pop_vote.jpg")



pres_pt_diff = pres_pt.groupby(level=1).diff()

pres_pt_diff_2020 = pres_pt_diff.loc[2020]
pres_pt_diff_2020_pop = pres_pt_diff_2020.drop("MARGIN", axis=1).join(fips_key.POP_ESTIMATE_2020)
pres_pt_diff_2020_pop = pres_pt_diff_2020_pop.div(pres_pt_diff_2020_pop.POP_ESTIMATE_2020, axis=0)
pres_pt_diff_2020_pop_zscore = pres_pt_diff_2020_pop.loc[:, utils.major_total].dropna().transform(utils.zscore_all_cols)

vote_2020_DEM_pop_adj_outliers = (pres_pt_diff_2020_pop_zscore.DEMOCRAT > 2)


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


mask = benford.mask_45
counties_on_both_lists_2020 = fips_key.loc[(mask & vote_2020_DEM_pop_adj_outliers)].drop("POP_ESTIMATE_2020", axis=1).join(pres_pt_diff_2020)


# now lets build a training dataset for 2020 that flags outliers
# margin_2020, margin_chg_2020, margins_chg_3, total_pct_pop, total_vote (needs log normalized), dem_vote_pct_pop, rep_vote_pct_pop, dem_pct_chg, rep_pct_chg

def flipped(df, axis=1):
    curr = df > 0
    prev = df.shift(axis=axis).dropna(axis=axis, how='all') > 0
    return curr ^ prev

d = dict(
    margin = pres_pt.loc[2020, "MARGIN"],
    margin_chg = pres_pt_diff.loc[2020, "MARGIN"],
    margin_chg_3 = pres_pt_diff.groupby(level=1).rolling(3).mean().xs(2020, level=1)["MARGIN"].droplevel(1),
    flipped = pres_pt['MARGIN'].unstack(0).transform(flipped)[2020],
    total_vote_pct_pop = pres_pt_diff_2020_pop["TOTAL"],
    total_vote = pres_pt.loc[2020, "TOTAL"],
    dem_vote_diff_pct_pop = pres_pt_diff_2020_pop["DEMOCRAT"],
    rep_vote_diff_pct_pop = pres_pt_diff_2020_pop["REPUBLICAN"],
    dem_vote_pct_chg = pres_pt.groupby(level=1).pct_change(fill_method=None).loc[2020, "DEMOCRAT"],
    rep_vote_pct_chg = pres_pt.groupby(level=1).pct_change(fill_method=None).loc[2020, "REPUBLICAN"],
    benford_anom = mask
)




dataset = pd.DataFrame(d)
dataset = dataset.assign(margin_chg_grew = (dataset.margin_chg - dataset.margin_chg_3).abs() > 0)
dataset = dataset.assign(margin_chg_shift = dataset.margin_chg-dataset.margin_chg_3)
mean = dataset.mean()
dataset = dataset.fillna(mean)

pt = PowerTransformer(method="box-cox")
nt = Normalizer()

exp_features = ["total_vote"]
normal_features = set(dataset.columns) - set(exp_features)

ct = ColumnTransformer([
        ("lt", pt, exp_features),
        ('nt', nt, list(normal_features))
     ]
)

svm = OneClassSVM()
isf = IsolationForest()
cluster = KMeans(n_clusters = 5, random_state=42)

pipe = Pipeline(
    [("ct", ct), ("out_clf", isf)]
)

cluster_pipe = Pipeline(
    [("ct", ct), ("cluster", cluster)]
)


# optimize for K using elbow and silhouette score
#tests = []
#for k in range(3,15):
#    cluster_pipe.set_params(**{'cluster__n_clusters' : k})
#    cluster_pipe.fit(dataset)
#    wcss = cluster_pipe[1].inertia_
#    sc = silhouette_score(dataset, cluster_pipe[1].labels_)
#    tests.append((k, wcss, sc))

# best appears to be 7

#test_data = pd.DataFrame(tests, columns = ['k', 'wcss', 'sc']).set_index("k" ,drop=True)
#ax = test_data.wcss.plot(kind='line')
#test_data.sc.plot(kind='line', secondary_y=True, ax=ax)
#ax.figure.show()

cluster_pipe.set_params(**{'cluster__n_clusters' : 7})
cluster_7 = pd.Series(cluster_pipe.fit_predict(dataset), index=dataset.index)

outliers_isf = dataset.loc[pipe.fit_predict(dataset)==-1]


outliers_isf = outliers_isf.join(fips_key)
outliers_isf['shift'] = pd.cut(outliers_isf.margin, [-np.inf, 0, np.inf], labels=['left', 'right'])
num_cols = list(outliers_isf.select_dtypes(include = np.number).columns)
agg_func = dict(zip(
    num_cols,
    ['mean']*4 + ['sum']+["mean"]*4+['sum']
    )
)
named_cols = dict(zip([tup for tup in agg_func.items()], agg_func.items()))
agg_func.update(county_name = 'count')
new_index = pd.MultiIndex.from_tuples(zip(agg_func.values(), num_cols+['county_name']))
outliers_sum = outliers_isf.groupby('shift').agg(agg_func)
outliers_sum.columns = new_index

fips_key = fips_key.assign(cluster=cluster_7)
num_cols = list(fips_key.select_dtypes(include=np.number).columns)

size_sum = dataset.join(fips_key[['size', "POP_ESTIMATE_2020", "county_name"]]).groupby("size").agg(agg_func)
size_sum.columns = list(named_cols.keys()) + [("county_name", "count")]

def pct_true(s):
    return s.sum()/s.count()

cluster_named_agg = dict(
    pop_mean = ("POP_ESTIMATE_2020", 'mean'),
    county_ct = ("county_name", 'count'),
    margin_mean = ("margin", 'mean'),
    margin_std = ("margin", 'std'),
    margin_chg_3 = ("margin_chg_3", 'mean'),
    dem_vote_diff_pct_pop = ('dem_vote_diff_pct_pop', 'mean'),
    dem_vote_pct_chg = ("dem_vote_pct_chg", "mean"),
    rep_vote_pct_chg = ('rep_vote_pct_chg', 'mean'),
    flipped_pct = ('flipped', pct_true),
    margin_chg_grew = ("margin_chg_grew", pct_true),
)

cluster_sum = dataset.join(fips_key[['POP_ESTIMATE_2020', 'county_name', 'cluster']]).groupby("cluster").agg(**cluster_named_agg)
cluster_sum.to_excel("../tabs/cluster_sum.xlsx")
cluster_describe = dataset.join(fips_key[['POP_ESTIMATE_2020', 'county_name', 'cluster']]).groupby("cluster").describe()
#cluster_sum.join(cluster_describe).to_excel("../tabs/cluster_sum.xlsx")


cluster_7.name = 'cluster'
plot_cols = ['margin', 'margin_chg', 'margin_chg_3', 'dem_vote_pct_chg', "dem_vote_diff_pct_pop", 'benford_anom']
plot_set = pd.concat([dataset[plot_cols], np.log(dataset.total_vote), cluster_7], axis=1)
g = sns.pairplot(plot_set, hue='benford_anom')
#g.map_lower(sns.kdeplot, levels=4)
g.savefig("../img/pairgrid.jpg")
g.figure.show()

ax = sns.catplot(plot_set, x='margin', y='cluster')

# clusters on size
# v_small - 0, 5 - small, 4 - wide_range, 3 - urban, 1 suburban
dataset = dataset.join(cluster_7).assign(log_pop=np.log(dataset.total_vote))
corr = dataset.corr()
# vote_margin - 4 - very left.  3 - moderate, hard left.  5 - middle and right, 0 - lean right, 6 -left, 2 - solid right 1 moderate

# I just added random_state to Kmeans so class labels will be reproducible.
cluster_desc = """
    0, Rural, very red and reliable, very low flips
    1, Lg Suburban, leans right but lurched left, high flip rate
    2, Suburban, reliably red, no flips
    3, Urban, blue and lurched left, very high flip rate
    4, Suburban, very red, low fips
    5, Small town, reliably left, medium flips
    6, Small town, very reliably right, no flips
    """.split("\n")
cluster_desc = [tuple(item.lstrip().split(', ')) for item in cluster_desc][1:-1]
cluster_desc = pd.DataFrame(cluster_desc, columns = ['cluster', 'urban', 'political', '16_20_vote_flips']).astype({"cluster": int}).set_index('cluster', drop =True)
cluster_desc.to_csv("../tabs/cluster_desc.csv")

yr_ndx = set(pres_pt.index.get_level_values(0))
p_data = pres_pt.unstack(0)["MARGIN"].join(mask).join(cluster_7).melt(value_vars=yr_ndx, id_vars=["BAG", 'cluster'], var_name='year', value_name = 'margin')
ax = sns.lineplot(data=p_data, x="year", y='margin', hue="cluster")
ax.figure.show()

cond = (dataset.benford_anom)