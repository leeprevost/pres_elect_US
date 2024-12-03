


## Methods:
1) used python pandas to analyze presidential election data from 2000.
2) Created margin column that shows vote margins between two major parties (negative for Dem, positive for Rep).

data sourced from: [Harvard Dataverse sourced via MIT Election Lab](https://dataverse.harvard.edu/dataset.xhtml?persistentId=doi:10.7910/DVN/VOQCHQ)


## Vote Margins
- (pres_pt.REPUBLICAN - pres_pt.DEMOCRAT)/pres_pt.TOTAL
- negative values - democrat majority vote
- positive values -- republican majority vote

## Bins:
Counties binned into roughly equal vote blocks of 5 which resulted in the following distribution (counts):


| size   |   count |
|:-------|--------:|
| xs     |    2537 |
| s      |     382 |
| m      |     140 |
| l      |      68 |
| xl     |      27 |



![vote_distro](/img/us_pop_vote.jpg)