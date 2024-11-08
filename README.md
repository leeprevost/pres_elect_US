# PRESIDENTIAL Election Anaylsis (2020-    )
by: Lee Prevost

I did a very quick analysis using data sourced from: date source: https://dataverse.harvard.edu/dataset.xhtml?persistentId=doi:10.7910/DVN/VOQCHQ

Used python pandas to read presidential election data from 2020.   Created margin column that shows vote margins as a percent of total vote such that:
(pres_pt.REPUBLICAN - pres_pt.DEMOCRAT)/pres_pt.TOTAL
negative values - county voted for democrat majority vote
positive values -- county voted for republican majority vote

xs, s, m, l, xl are binned out via a logarithmic bin

I do see some oddities at county levels particuarly in Georgia in 2020 in larger/suburban counties with large shifts to the left and in Texas in small/rural counties with large shifts to right.

But, I also can't get to the 80M+ votes Zero Hedge chart shows for Democrats in 2020.  Am I missing something?



