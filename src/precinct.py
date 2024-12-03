import pandas as pd
import utils

#precinct level data from MIT/harvard dataverse
#
prec_16_src = r"C:\Users\lee\Downloads\2016-precinct-president.csv"
prec_20_src = r"C:\Users\lee\Downloads\PRESIDENT_precinct_general.csv"

dt = dict(
    county_fips=str,
)

prec_16 = pd.read_csv(prec_16_src, encoding = 'latin-1', low_memory=False, dtype=dt)
prec_20 = pd.read_csv(prec_20_src, encoding = 'latin-1', low_memory=False, dtype=dt)


cond_list = ["ABSENTEE", "ABSENTEE BY MAIL", '2ND ABSENTEE', "MAIL", "PROVISIONAL", "MAIL BALLOTS", "FAILSAFE PROVISIONAL", "FAILSAFE"]
cond = prec_20['mode'].isin(cond_list)

for d in [prec_16, prec_20]:
    d['county_fips']= d['county_fips'].apply(utils.fix_fips)


cond_votes =  prec_20.loc[cond].groupby("county_fips")['votes'].sum()

total_votes = prec_20[prec_20['mode']=='TOTAL'].groupby('county_fips')['votes'].sum()

votes_by_mode = prec_20.groupby('mode')['votes'].sum().sort_values()
cond_pct_vote = cond_votes/total_votes