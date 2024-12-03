from src import vote_data
import seaborn as sns

pres_pt = vote_data.pres_pt

votes_20 = pres_pt.loc[2020, "TOTAL"].reset_index()

ax = sns.histplot(votes_20, x="TOTAL", log_scale=True)
ax.figure.suptitle(f"Distribution of 2020 Total Votes By County (n={len(votes_20):,.0f})\n@leeprevost")
ax.text(x=1e5, y = 200, s= f"Min: {votes_20.TOTAL.min():,.0f}\nMax: {votes_20.TOTAL.max():,.0f} ")
ax.figure.savefig("../img/vote_distro.jpg")
ax.figure.show()

