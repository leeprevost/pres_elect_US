# How Does County Level Election Data Fit Benford's Law?
Although Benford has many use cases including detection of election fraud, it does seem to be controversial particularly
among the academics.

Walter Mebane, a professor at University of Michigan and an authority on the use of Benford's Law and other forensic measures 
on election integrity, has offered an R based [toolset](https://github.com/UMeforensics/eforensics_public) to investigate
election datasets.   Walter has provided a very helpful guide to [innapropriate](https://websites.umich.edu/~wmebane/inapB.pdf) uses of Benford's Law on election data including its
use on precinct level data.

Dr. Jen Golbeck [scolded](https://x.com/jengolbeck/status/1852531635662565599) us on X:
- "They are wrong. NEITHER follow it…because Benford doesn't work on elections"
- "You simply cannot use a first-digit Benford's Law analysis to prove election fraud, and even if it worked, the people applying it aren't even doing it right. Doing actual math and statistics requires very precise work, not just tossing some numbers into a spreadsheet"
- "Most people don't have the background to understand or challenge it."

Of course, she did this right before election day (Nov 1) and used right leaning examples (which were wrong) as her exhibits.

Using Benford's Law to calculate the frequency of first digits on county level election data:
![benford_facet](C:\Users\lee\PycharmProjects\pres_elect_US\img\benford_facet.jpg)

Its very difficult for me to see how Benford doesn't fit the county level data.  I'm certinaly open to argument from experts
rather than partisans.   Blue line is the expected result.  Bars are the actual result.  Error statistics 
are shown in the graph including mean absolute error.    R2 is shown but I realize now that a better error stat should be something like
Chisquare or CVM.   The error stats and p-values for Chisquare are shown here:

|                        |        cs |        p_value |
|:-----------------------|----------:|---------------:|
| ('DEMOCRAT', 2000)     |  26.5271  |    0.000852902 |
| ('DEMOCRAT', 2004)     |  20.4004  |      0.0089228 |
| ('DEMOCRAT', 2008)     |  13.6428  |      0.0915644 |
| ('DEMOCRAT', 2012)     |  14.9458  |      0.0602078 |
| ('DEMOCRAT', 2016)     |  13.4589  |      0.0970049 |
| **('DEMOCRAT', 2020)** |  21.4092  | **0.00613625** |
| ('GREEN', 2000)        |   4.3741  |       0.821893 |
| ('GREEN', 2004)        | nan       |            nan |
| ('GREEN', 2008)        | nan       |            nan |
| ('GREEN', 2012)        | nan       |            nan |
| ('GREEN', 2016)        | nan       |            nan |
| ('GREEN', 2020)        |   5.66681 |       0.684497 |
| ('LIBERTARIAN', 2000)  | nan       |            nan |
| ('LIBERTARIAN', 2004)  | nan       |            nan |
| ('LIBERTARIAN', 2008)  | nan       |            nan |
| ('LIBERTARIAN', 2012)  | nan       |            nan |
| ('LIBERTARIAN', 2016)  | nan       |            nan |
| ('LIBERTARIAN', 2020)  |   6.14041 |       0.631507 |
| ('OTHER', 2000)        |  12.1267  |       0.145641 |
| ('OTHER', 2004)        |  20.0392  |      0.0101889 |
| ('OTHER', 2008)        |   8.42569 |       0.393029 |
| ('OTHER', 2012)        |   9.15816 |        0.32913 |
| ('OTHER', 2016)        |   2.11137 |       0.977406 |
| ('OTHER', 2020)        |  11.0579  |       0.198442 |
| ('REPUBLICAN', 2000)   |  18.1816  |      0.0199053 |
| ('REPUBLICAN', 2004)   |  10.5621  |       0.227764 |
| ('REPUBLICAN', 2008)   |  10.5745  |       0.226992 |
| ('REPUBLICAN', 2012)   |  13.3614  |       0.100005 |
| ('REPUBLICAN', 2016)   |  13.5881  |      0.0931536 |
| ('REPUBLICAN', 2020)   |   9.62145 |       0.292607 |
| ('TOTAL', 2000)        |  17.1179  |      0.0289046 |
| ('TOTAL', 2004)        |  13.3447  |       0.100526 |
| ('TOTAL', 2008)        |  21.0925  |     0.00690581 |
| ('TOTAL', 2012)        |  27.6949  |     0.00053588 |
| ('TOTAL', 2016)        |  17.8239  |      0.0225864 |
| ('TOTAL', 2020)        |  25.8515  |     0.00111352 |

For my purposes, the p-value on the Democrat vote in 2020 rules out the null hypothesis (that Benford doesn't fit).  It also shows
a higher than normal error rate.

The election digit count frequencies and their errorbars at 2$\sigma$ are shown plotted with the expected Benford frequencies (orange):
![](C:\Users\lee\PycharmProjects\pres_elect_US\img\election_freq.jpg)

It looks like a decent fit to me!

But, the 2020 Democrat vote looks off to me -- particularly on digit 4/5.  
![](C:\Users\lee\PycharmProjects\pres_elect_US\img\benford_20_dem.jpg)

Lets investigate further.








