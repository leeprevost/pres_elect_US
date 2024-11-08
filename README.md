# PRESIDENTIAL Election Anaylsis (2020-2024)
by: Lee Prevost, 11/7/2024

Inspired by the questions raised by this graph posted by ZeroHedge:
![What Happend Here?](/zero_hedge.png)


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



![vote_distro](/us_pop_vote.jpg)

Very specifically, I wanted to focus on where the incremental votes for Joe Biden came from over the Democrat vote counts
in the 2016 election, by county.   The raw counts for those vote diffs are in: [diff_16_20.csv](/diff_16_20.csv).  Would 
love to see some additional analysis on this including zscore or Benford so as to see unnatural shifts (lurch leftward
or rightward).

But, as to raw counts of vote shifts, the top 30 counties represent 4.24M incremental votes over the 2016 election.

![Where Did Additional Biden Votes Come From Over 2016?](/inc_20_demo_votes.jpg)

Some incremental questions:
- Were there unusual (ie. unnatural) margin shifts at county level in 20 over 2000-2016?
- Possible use of Benford or Zscore to flush those out.
- Which counties lurched leftward or rightward in an unpredictable or unnatural way (20 over 00-16)?

Looking at margin shift over time [margin_shift_over_time.csv](/margin_shift_over_time.csv):
- looks very predictable.  Unusual patterns should be easy to spot
- Zscore/Benford?




