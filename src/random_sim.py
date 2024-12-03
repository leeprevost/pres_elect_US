import vote_data
import secrets
import numpy as np
import benford
import pandas as pd
import seaborn as sns
import utils
import matplotlib.pyplot as plt
from scipy.stats import norm
from scipy import stats


rng = np.random.default_rng(secrets.randbits(128))

rec_votes = vote_data.pres_pt.loc[2020, "TOTAL"]
vote_stats = rec_votes.describe()
log_stats = np.log(rec_votes).describe()

digit_counts = []
digit_freqs=[]
for sim in range(0, 1000):
    sim_votes = np.round(np.exp(rng.normal(log_stats['mean'], log_stats['std'], int(log_stats['count']))))
    digit_freq = benford.digit_counts(pd.Series(sim_votes))
    digit_freqs.append(digit_freq)
    digit_counts.append(digit_freq)

error_metric = benford.mean_absolute_error

def digit_error(col, metric = benford.r2_score):
    return metric(benford.benford_range, col)

sims_freqs = pd.concat(digit_freqs, axis=1)
sims = pd.concat(digit_counts, axis=1)
sims_error = sims.sub(benford.benford_range, axis=0)
sims_pct_error = sims_error.div(benford.benford_range, axis=0)
mae = sims.apply(lambda col: error_metric(benford.benford_range, col))
sims_r2 = sims.apply(digit_error)

sns.set()
p_data = benford.benford_raw.drop("benford_expected", axis=1).melt(ignore_index=False).reset_index()
ax = sns.pointplot(p_data, x='digits', y='value', label='actual', errorbar=('sd', 2), legend=True)
ax.plot(benford.benford_range.values, marker="_", markersize=20, label='expected')
ax.legend()
ax.figure.suptitle(f"2000-2020 First Digit Frequencies vs. Benford Expected\nErrorbars are 2{chr(963)}, @leeprevost")
ax.figure.savefig("../img/election_freq.jpg")
plt.legend()
ax.figure.show()


ax = sns.boxplot(sims_error.T.unstack().reset_index(), y=0, x='digits')
ax.figure.suptitle("Distribution of Digit Errors Simulation")
ax.set_ylabel("Error")
ax.yaxis.set_major_formatter(utils.pct_formatter)

ax.figure.show()


(sims_error > .017).loc[4.0].sum()
# 2/1000 for 4 digit error above 0.017
# 2/1000 for 5 digit error above 0.013
# prob of both??

prob_mae = lambda x: tuple((x, (mae > x).sum()))

mae_probs = list(map(prob_mae, benford.mad_range[0:-1]))
# mae > .007, 17/1000
# mae > .005, 227/1000

benford_errors = benford.benford_raw_ae
benford_major_total_r2_errors = benford.benford_r2[vote_data.major_total]
benford_mae = benford_errors.abs().mean()
benford_20_total = benford_mae["TOTAL"][2020]
benford_20_dem = benford_mae["DEMOCRAT"][2020]


p_data = pd.concat([sims_r2.to_frame().assign(sim="Random"), benford_major_total_r2_errors.to_frame().assign(sim="Actual")]).rename(columns = {0: "R2"})
ax = sns.boxplot(x=p_data['sim'], y=p_data["R2"],flierprops={'marker': 'None'})
ax.figure.suptitle("Actual Election Results (2000-2020) R2 Fit to Benford")
ax.set_ylim((.9825,1))
ax.figure.tight_layout()
ax.figure.savefig("../img/election_benford_r2_vs_sim.jpg")
ax.set_xlabel("")
utils.footnote(ax, x=0.05, s= "Actual: Includes all major parties and total votes 2000-2020.\nRandom: 1000 simulations of ~3200 counties with random lognormal data.", size='x-small')
utils.footnote(ax)
ax.figure.show()

dem_20_digit_errors = benford_errors["DEMOCRAT"][2020][4.0:5.0]

# fit scipy stats norm to errors
loc, scale = norm.fit(sims_error.stack())
prob = lambda x: norm.sf(x, loc, scale)

prob_errors = list(map(prob, dem_20_digit_errors.abs() ))
probboth = prob_errors[0] * prob_errors[1]
# mae errors
arrowprops=dict(facecolor='black', shrink=0.05)
ax = sns.histplot(mae)
ax.figure.suptitle("Distribution of Mean Absolute Errors\n Simulation of 1000 County Votes")
ax.xaxis.set_major_formatter(utils.pct_formatter)
ax.annotate("Actual 2020\nTotal Error", xy=(benford_20_total, 5), xytext=(benford_20_total, 80), arrowprops = arrowprops)
ax.figure.savefig("../img/mae_errors_sim.jpg")
ax.figure.show()

# actual digit errors 2020
ax = sns.histplot(sims_error.stack())
ax.figure.suptitle("Distribution of Digit Errors\nSimulation of 1000 County Votes")
ax.xaxis.set_major_formatter(utils.pct_formatter)
ax.annotate("Actual 2020\n5 Digit Error", xy=(dem_20_digit_errors[5], 5), xytext=(dem_20_digit_errors[5], 400), arrowprops =arrowprops)
ax.annotate("Actual 2020\n4 Digit Error", xy=(dem_20_digit_errors[4], 5), xytext = (dem_20_digit_errors[4], 400), arrowprops = arrowprops)
plt.figtext(0.5, 0.01, "Probability of Both Errors: 0 occurrences in 9000 error samples", ha="center")
ax.figure.savefig("../img/digit_errors_sim.jpg")
ax.figure.show()

tot_errors = sims_error.stack().shape[0]
mask_4= (sims_error.stack() >= dem_20_digit_errors[4])
mask_5 = (sims_error.stack() <= dem_20_digit_errors[5])
both = mask_4 & mask_5
# 0 times over 9000 errors
prob_4 = mask_4.sum()/tot_errors
prob_5 = mask_5.sum()/tot_errors
prob_both = prob_4 * prob_5
# calc prob is 14/1m


all_benford_errors = benford_errors.stack().stack()
tot_b_errors = all_benford_errors.shape[0]
prob_both_actual = ((all_benford_errors >= dem_20_digit_errors[4]) & (all_benford_errors <= dem_20_digit_errors[5])).value_counts()
prob_both_actual_calc = (all_benford_errors >= dem_20_digit_errors[4]).sum()/tot_b_errors * (all_benford_errors <= dem_20_digit_errors[5]).sum()/tot_b_errors




