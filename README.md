# PRESIDENTIAL Election Anaylsis (2020-    )
by: Lee Prevost, 11/7/2024

I did a very quick analysis using data sourced from: [Harvard Dataverse sourced via MIT Election Lab](https://dataverse.harvard.edu/dataset.xhtml?persistentId=doi:10.7910/DVN/VOQCHQ)

Used python pandas to read presidential election data from 2020.   Created margin column that shows vote margins as a percent of total vote such that:
(pres_pt.REPUBLICAN - pres_pt.DEMOCRAT)/pres_pt.TOTAL
negative values - county voted for democrat majority vote
positive values -- county voted for republican majority vote


Bins:
- 66.0
- 604.8
- 5542.0
- 50784.4
- 465363.5
- 4264365.0

Corresponding labels
- xs
- s
- m
- l
- xl


I do see some oddities at county levels particuarly in Georgia in 2020 in larger/suburban counties with large shifts to the left and in Texas in small/rural counties with large shifts to right.


![vote_distro](/us_pop_vote.jpg)

Very specifically, I wanted to focus on where the incremental votes for Joe Biden came from over the Democrat vote counts
in the 2016 election, by county.   The raw counts for those vote diffs are in: [diff_16_20.csv](/diff_16_20.csv).  Would 
love to see some additional analysis on this including zscore or Benford so as to see unnatural shifts (lurch leftward
or rightward).

But, as to raw counts of vote shifts, the top 30 counties represent 4.24M incremental votes over the 2016 election.


![Where Did Additional Biden Votes Come From Over 2016?](/inc_20_demo_votes.jpg)






