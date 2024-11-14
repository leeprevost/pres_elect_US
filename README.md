# PRESIDENTIAL Election Anaylsis (2020-2024)
by: Lee Prevost, 11/7/2024

Inspired by the questions raised by this graph posted by ZeroHedge:
![What Happend Here?](/img/zero_hedge.png)

First, I'll acknowledge a few things about the chart.  The y-axis range is bound limited which has the effect of 
exaggerating the change over the years.   Also, others have pointed out correctly that the 2024 year doesn't have complete data
yet.  

Nevertheless, none of those critiques take away from the core rhetorical question: what explains the gap of votes for Biden 
over 2016 in the 2020 election?  

The question:
![vote change from 2016-2020](/img/the_question.png)

This question intrigued me.

Also, inspired by the recent NYT visuals that show the "shift left/right" vectors on a map:
![NYT vector map](/img/Gbuf-iqXcBAXUaB.jpg)



## Methods:
1) used python pandas to read presidential election data from 2000.   
2) Created margin column that shows vote margins as a percent of total vote such that: 

data sourced from: [Harvard Dataverse sourced via MIT Election Lab](https://dataverse.harvard.edu/dataset.xhtml?persistentId=doi:10.7910/DVN/VOQCHQ)


## Vote Margins
(pres_pt.REPUBLICAN - pres_pt.DEMOCRAT)/pres_pt.TOTAL
negative values - democrat majority vote
positive values -- republican majority vote

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

Very specifically, I wanted to focus on where the incremental votes for Joe Biden came from over the Democrat vote counts
in the 2016 election, by county.   The raw counts for those vote diffs are in: [diff_16_20.csv](/tabs/diff_16_20.csv).  

The top 30 counties whose votes shifted towards Biden include 4.24M incremental votes over the 2016 election.

![Where Did Additional Biden Votes Come From Over 2016?](/img/inc_20_demo_votes.jpg)

Some incremental questions:
~~- Were there unusual (ie. unnatural) margin shifts at county level in 20 over 2000-2016?~~
- Possible use of Benford or Zscore to flush those out.  (@todo: Benford)
~~- Which counties lurched leftward or rightward in an unpredictable or unnatural way (20 over 00-16)?~~

## Distribution of Margins By County
Analyis to think about how to suss out the outliers, looking at what looks to be fairly normal distribution of margins across all
3,156 counties.    This is a frequency count, not magnitude showing that most of US counties are steadily shifting right but 
most of those are small.

Shifting right -- positive
Shifting left -- negative
![margin_distro](/img/distribution_vote_margins_county.jpg)


## Outliers - 2020 Vote
Outliers were determined by performing a zscore on entire margin_over_time dataset and selecting those 
counties in 2020 that had an abs(zscore) > 2. This resulted in the [outliers_2020_vote.csv](/tabs/outliers_2020_vote.csv) tabulation.

|                                     |        2000 |       2004 |       2008 |      2012 |      2016 |      2020 |
|:------------------------------------|------------:|-----------:|-----------:|----------:|----------:|----------:|
| ('DC', 'DISTRICT OF COLUMBIA', 'l') | -0.762034   | -0.798441  | -0.859246  | -0.836348 | -0.867763 | -0.867524 |
| ('MD', "PRINCE GEORGE'S", 'l')      | -0.610984   | -0.643695  | -0.784873  | -0.805181 | -0.797259 | -0.805258 |
| ('SD', 'OGLALA LAKOTA', 's')        |  0.17545    |  0.22551   |  0.160772  |  0.234293 | -0.781067 | -0.79125  |
| ('MD', 'BALTIMORE CITY', 'l')       | -0.684055   | -0.649888  | -0.754993  | -0.761036 | -0.741297 | -0.765962 |
| ('VA', 'PETERSBURG CITY', 'm')      | -0.600434   | -0.622981  | -0.784492  | -0.801861 | -0.76672  | -0.764523 |
| ('NY', 'NEW YORK', 'xl')            | -0.65582    | -0.631024  | -0.722675  | -0.672043 | -0.768507 | -0.738311 |
| ('VA', 'CHARLOTTESVILLE CITY', 'm') | -0.281912   | -0.447638  | -0.580074  | -0.535211 | -0.664872 | -0.726965 |
| ('CA', 'SAN FRANCISCO', 'l')        | -0.594404   | -0.681082  | -0.705021  | -0.704985 | -0.757521 | -0.725368 |
| ('AK', 'DISTRICT 99', 'xs')         |  0.17545    |  0.22551   |  0.160772  |  0.234293 | -0.684211 | -0.725173 |
| ('MS', 'JEFFERSON', 's')            | -0.641432   | -0.631105  | -0.745414  | -0.785698 | -0.737565 | -0.715455 |
| ('MS', 'CLAIBORNE', 's')            | -0.6039     | -0.638414  | -0.721967  | -0.768235 | -0.741573 | -0.712295 |
| ('GA', 'CLAYTON', 'l')              | -0.32696    | -0.414942  | -0.663941  | -0.700709 | -0.706178 | -0.709099 |
| ('LA', 'ORLEANS', 'l')              | -0.542023   | -0.556881  | -0.601564  | -0.625544 | -0.661617 | -0.681536 |
| ('VA', 'RICHMOND CITY', 'l')        | -0.340564   | -0.410764  | -0.590579  | -0.572631 | -0.634668 | -0.67972  |
| ('GA', 'DEKALB', 'l')               | -0.435049   | -0.460699  | -0.586449  | -0.567587 | -0.635099 | -0.673817 |
| ('CA', 'MARIN', 'l')                | -0.359409   | -0.479488  | -0.577302  | -0.513069 | -0.624213 | -0.665315 |
| ('NY', 'BRONX', 'l')                | -0.745196   | -0.650864  | -0.777836  | -0.83021  | -0.790567 | -0.665205 |
| ('MO', 'ST. LOUIS CITY', 'l')       | -0.575205   | -0.610766  | -0.681508  | -0.667356 | -0.635737 | -0.661963 |
| ('WI', 'MENOMINEE', 's')            | -0.587186   | -0.65731   | -0.740331  | -0.734931 | -0.573886 | -0.644654 |
| ('MS', 'HOLMES', 'm')               | -0.472918   | -0.521243  | -0.635409  | -0.686585 | -0.666171 | -0.64313  |
| ('VA', 'FALLS CHURCH CITY', 'm')    | -0.174861   | -0.306658  | -0.403704  | -0.394173 | -0.579477 | -0.641343 |
| ('AL', 'MACON', 'm')                | -0.744423   | -0.662273  | -0.740462  | -0.742159 | -0.671225 | -0.638198 |
| ('PA', 'PHILADELPHIA', 'xl')        | -0.620519   | -0.611371  | -0.667581  | -0.713197 | -0.671645 | -0.635372 |
| ('VA', 'ARLINGTON', 'l')            | -0.259757   | -0.362937  | -0.445907  | -0.39789  | -0.591895 | -0.635052 |
| ('AL', 'GREENE', 's')               | -0.603731   | -0.590986  | -0.665787  | -0.696067 | -0.650615 | -0.630157 |
| ('MA', 'SUFFOLK', 'l')              | -0.508972   | -0.530528  | -0.556914  | -0.566925 | -0.632666 | -0.628363 |
| ('VA', 'ALEXANDRIA CITY', 'l')      | -0.264316   | -0.345802  | -0.444716  | -0.435221 | -0.580137 | -0.626459 |
| ('CA', 'ALAMEDA', 'xl')             | -0.452344   | -0.520157  | -0.595062  | -0.606912 | -0.64029  | -0.625073 |
| ('NC', 'DURHAM', 'l')               | -0.280802   | -0.363973  | -0.51939   | -0.527856 | -0.595002 | -0.623792 |
| ('CO', 'DENVER', 'l')               | -0.309906   | -0.403198  | -0.524117  | -0.49357  | -0.548018 | -0.613655 |
| ('OR', 'MULTNOMAH', 'l')            | -0.353115   | -0.444303  | -0.560788  | -0.547225 | -0.56278  | -0.613067 |
| ('CA', 'SANTA CRUZ', 'l')           | -0.341403   | -0.482597  | -0.576555  | -0.555877 | -0.565211 | -0.602809 |
| ('MD', 'MONTGOMERY', 'xl')          | -0.290225   | -0.331391  | -0.445831  | -0.438707 | -0.55366  | -0.596442 |
| ('MO', 'KANSAS CITY', 'l')          |  0.17545    | -0.484815  | -0.57596   | -0.556724 | -0.568277 | -0.594731 |
| ('CA', 'SAN MATEO', 'l')            | -0.333313   | -0.403436  | -0.487217  | -0.466642 | -0.572399 | -0.576918 |
| ('MA', 'DUKES', 'm')                | -0.356707   | -0.46644   | -0.518431  | -0.47283  | -0.514954 | -0.565758 |
| ('CO', 'BOULDER', 'l')              | -0.136866   | -0.338936  | -0.461421  | -0.418442 | -0.483348 | -0.565656 |
| ('SD', 'TODD', 's')                 | -0.344712   | -0.469353  | -0.583185  | -0.59191  | -0.479059 | -0.563608 |
| ('NJ', 'ESSEX', 'l')                | -0.457147   | -0.415787  | -0.527749  | -0.568321 | -0.571378 | -0.554124 |
| ('NM', 'TAOS', 'm')                 | -0.394218   | -0.493495  | -0.648466  | -0.602908 | -0.52038  | -0.547465 |
| ('VT', 'CHITTENDEN', 'l')           | -0.181221   | -0.295343  | -0.447915  | -0.415867 | -0.434115 | -0.54606  |
| ('NY', 'KINGS', 'xl')               | -0.649586   | -0.487023  | -0.594538  | -0.639625 | -0.620042 | -0.543838 |
| ('CO', 'SAN MIGUEL', 's')           | -0.170507   | -0.447126  | -0.555402  | -0.431861 | -0.448602 | -0.541675 |
| ('NM', 'SANTA FE', 'l')             | -0.364719   | -0.432145  | -0.550517  | -0.510824 | -0.510415 | -0.537548 |
| ('WA', 'KING', 'xl')                | -0.256309   | -0.312618  | -0.421367  | -0.405627 | -0.502738 | -0.52717  |
| ('WI', 'DANE', 'l')                 | -0.285844   | -0.330659  | -0.46978   | -0.435356 | -0.471739 | -0.526072 |
| ('MS', 'NOXUBEE', 'm')              | -0.374041   | -0.431063  | -0.532675  | -0.573914 | -0.564586 | -0.524443 |
| ('SC', 'ALLENDALE', 's')            | -0.410479   | -0.439989  | -0.517396  | -0.59068  | -0.541759 | -0.524075 |
| ('CO', 'PITKIN', 'm')               | -0.201538   | -0.383684  | -0.48816   | -0.379653 | -0.454528 | -0.519277 |
| ('CA', 'SONOMA', 'l')               | -0.272916   | -0.363768  | -0.496013  | -0.457988 | -0.471462 | -0.514738 |
| ('NC', 'ORANGE', 'l')               | -0.263274   | -0.345097  | -0.447737  | -0.421616 | -0.50238  | -0.510818 |
| ('WA', 'SAN JUAN', 'm')             | -0.168685   | -0.327022  | -0.419333  | -0.378894 | -0.416187 | -0.505266 |
| ('IL', 'COOK', 'xl')                | -0.399808   | -0.411001  | -0.533944  | -0.493635 | -0.53676  | -0.502999 |
| ('AL', 'BULLOCK', 's')              | -0.400082   | -0.363791  | -0.483841  | -0.527997 | -0.507431 | -0.498591 |
| ('NY', 'TOMPKINS', 'm')             | -0.211083   | -0.285836  | -0.421302  | -0.370078 | -0.433924 | -0.48912  |
| ('AL', 'SUMTER', 'm')               | -0.457622   | -0.411472  | -0.503276  | -0.545752 | -0.493683 | -0.48482  |
| ('MS', 'HINDS', 'l')                | -0.102951   | -0.198238  | -0.390679  | -0.436168 | -0.446964 | -0.484114 |
| ('AL', 'PERRY', 's')                | -0.395369   | -0.367373  | -0.451047  | -0.50205  | -0.457939 | -0.482027 |
| ('CA', 'SANTA CLARA', 'xl')         | -0.262238   | -0.29373   | -0.408964  | -0.429138 | -0.521321 | -0.474122 |
| ('MA', 'BERKSHIRE', 'l')            | -0.372473   | -0.473833  | -0.524452  | -0.536411 | -0.414718 | -0.468727 |
| ('MI', 'WASHTENAW', 'l')            | -0.235877   | -0.279908  | -0.409545  | -0.359025 | -0.412837 | -0.466204 |
| ('MA', 'HAMPSHIRE', 'l')            | -0.281832   | -0.408011  | -0.455586  | -0.439581 | -0.404757 | -0.465075 |
| ('GA', 'FULTON', 'xl')              | -0.179205   | -0.193629  | -0.349739  | -0.297791 | -0.415558 | -0.464881 |
| ('MS', 'TUNICA', 's')               | -0.315723   | -0.386856  | -0.523248  | -0.591511 | -0.508551 | -0.464346 |
| ('VT', 'WASHINGTON', 'm')           | -0.128845   | -0.245357  | -0.409783  | -0.418262 | -0.341022 | -0.464091 |
| ('NJ', 'HUDSON', 'l')               | -0.44456    | -0.352612  | -0.47005   | -0.560692 | -0.523642 | -0.463294 |
| ('ND', 'SIOUX', 's')                | -0.43708    | -0.425439  | -0.674891  | -0.590035 | -0.404221 | -0.460371 |
| ('AL', 'LOWNDES', 'm')              | -0.467564   | -0.406411  | -0.500137  | -0.530648 | -0.468582 | -0.458815 |
| ('VA', 'NORFOLK CITY', 'l')         | -0.263149   | -0.242553  | -0.429697  | -0.454258 | -0.425373 | -0.455583 |
| ('MN', 'RAMSEY', 'l')               | -0.207964   | -0.274234  | -0.338993  | -0.351974 | -0.391165 | -0.453562 |
| ('MA', 'NANTUCKET', 'm')            | -0.253756   | -0.273934  | -0.365169  | -0.268464 | -0.351858 | -0.453393 |
| ('CA', 'CONTRA COSTA', 'xl')        | -0.217483   | -0.258762  | -0.377609  | -0.352117 | -0.436169 | -0.453297 |
| ('MS', 'HUMPHREYS', 's')            | -0.167343   | -0.290045  | -0.424716  | -0.500767 | -0.451446 | -0.453091 |
| ('TX', 'TRAVIS', 'xl')              |  0.0521438  | -0.140154  | -0.294272  | -0.239334 | -0.386267 | -0.451091 |
| ('VT', 'WINDHAM', 'm')              | -0.18431    | -0.352076  | -0.481209  | -0.486803 | -0.392578 | -0.450091 |
| ('MA', 'MIDDLESEX', 'xl')           | -0.312198   | -0.294715  | -0.301247  | -0.271136 | -0.38336  | -0.448889 |
| ('NY', 'QUEENS', 'xl')              | -0.530489   | -0.437411  | -0.50537   | -0.59241  | -0.53596  | -0.448551 |
| ('MD', 'HOWARD', 'l')               | -0.0775588  | -0.0936627 | -0.218456  | -0.219682 | -0.339799 | -0.442708 |
| ('CA', 'LOS ANGELES', 'xl')         | -0.311142   | -0.275185  | -0.403655  | -0.418592 | -0.493439 | -0.44165  |
| ('GA', 'HANCOCK', 's')              | -0.567725   | -0.533239  | -0.630755  | -0.621086 | -0.518994 | -0.438415 |
| ('MA', 'FRANKLIN', 'm')             | -0.232842   | -0.387684  | -0.47664   | -0.469516 | -0.369699 | -0.437853 |
| ('MN', 'HENNEPIN', 'xl')            | -0.142794   | -0.198934  | -0.286095  | -0.270429 | -0.349303 | -0.432094 |
| ('IA', 'JOHNSON', 'l')              | -0.251568   | -0.292659  | -0.415142  | -0.35495  | -0.378945 | -0.428987 |
| ('MS', 'COAHOMA', 'm')              | -0.205904   | -0.294599  | -0.44356   | -0.481562 | -0.443447 | -0.428773 |
| ('VA', 'HAMPTON CITY', 'l')         | -0.165577   | -0.15459   | -0.389164  | -0.426019 | -0.375425 | -0.421335 |
| ('VT', 'LAMOILLE', 'm')             | -0.108483   | -0.277153  | -0.426192  | -0.419503 | -0.287651 | -0.421073 |
| ('GA', 'CLARKE', 'l')               | -0.114759   | -0.179025  | -0.313294  | -0.287753 | -0.375445 | -0.420821 |
| ('VA', 'FAIRFAX', 'xl')             |  0.0137273  | -0.0730224 | -0.211843  | -0.204993 | -0.35818  | -0.41837  |
| ('MS', 'LEFLORE', 'm')              | -0.157414   | -0.240757  | -0.367632  | -0.433101 | -0.410682 | -0.414854 |
| ('WA', 'JEFFERSON', 'm')            | -0.138075   | -0.266437  | -0.346256  | -0.319431 | -0.326445 | -0.414368 |
| ('CA', 'YOLO', 'l')                 | -0.174002   | -0.206641  | -0.362337  | -0.340342 | -0.414338 | -0.41427  |
| ('CA', 'MONTEREY', 'l')             | -0.20298    | -0.220027  | -0.382608  | -0.36861  | -0.40622  | -0.412718 |
| ('MS', 'SUNFLOWER', 'm')            | -0.191563   | -0.265446  | -0.411707  | -0.469362 | -0.409564 | -0.411321 |
| ('VA', 'WILLIAMSBURG CITY', 'm')    |  0.0142282  | -0.0351852 | -0.290997  | -0.286655 | -0.430239 | -0.410305 |
| ('MD', 'CHARLES', 'l')              | -0.00235468 | -0.0156591 | -0.255294  | -0.313685 | -0.303015 | -0.408858 |
| ('AK', 'DISTRICT 33', 'm')          |  0.463613   |  0.379594  |  0.503087  |  0.210547 | -0.326757 | -0.408581 |
| ('GA', 'ROCKDALE', 'm')             |  0.28987    |  0.215689  | -0.0956081 | -0.165603 | -0.25818  | -0.408003 |
| ('VA', 'PORTSMOUTH CITY', 'm')      | -0.272402   | -0.225123  | -0.393078  | -0.427747 | -0.362926 | -0.407906 |
| ('CA', 'NAPA', 'l')                 | -0.144304   | -0.205561  | -0.324687  | -0.286898 | -0.355015 | -0.403895 |
| ('VT', 'WINDSOR', 'm')              | -0.117576   | -0.229792  | -0.396599  | -0.379665 | -0.299084 | -0.403327 |
| ('NJ', 'MERCER', 'l')               | -0.26989    | -0.233938  | -0.363944  | -0.371452 | -0.374257 | -0.401412 |
| ('MS', 'WASHINGTON', 'm')           | -0.165757   | -0.197538  | -0.347788  | -0.422521 | -0.364695 | -0.399989 |
| ('GA', 'DOUGHERTY', 'm')            | -0.151459   | -0.181116  | -0.349791  | -0.391519 | -0.383695 | -0.39996  |
| ('WI', 'MILWAUKEE', 'l')            | -0.204914   | -0.243379  | -0.358537  | -0.360379 | -0.370135 | -0.398528 |
| ('OR', 'BENTON', 'l')               | -0.0946738  | -0.176123  | -0.314923  | -0.285367 | -0.323016 | -0.396769 |
| ('CO', 'SUMMIT', 'm')               | -0.0729129  | -0.201966  | -0.330156  | -0.246604 | -0.275566 | -0.39553  |
| ('KS', 'DOUGLAS', 'l')              | -0.0297957  | -0.161442  | -0.30842   | -0.246464 | -0.329567 | -0.394974 |
| ('NM', 'SAN MIGUEL', 'm')           | -0.47211    | -0.443216  | -0.605981  | -0.568859 | -0.462469 | -0.387391 |
| ('NM', 'MCKINLEY', 'm')             | -0.328169   | -0.27639   | -0.439092  | -0.46947  | -0.390361 | -0.386166 |
| ('SC', 'RICHLAND', 'l')             | -0.111735   | -0.150006  | -0.289117  | -0.319715 | -0.329127 | -0.38312  |
| ('VA', 'FAIRFAX CITY', 'm')         |  0.0419632  | -0.0331879 | -0.165292  | -0.161321 | -0.304655 | -0.38311  |
| ('MI', 'WAYNE', 'xl')               | -0.399925   | -0.395844  | -0.494766  | -0.468277 | -0.373408 | -0.381236 |
| ('VT', 'ADDISON', 'm')              | -0.113789   | -0.219065  | -0.391673  | -0.393858 | -0.311177 | -0.376896 |
| ('AL', 'DALLAS', 'm')               | -0.195353   | -0.206752  | -0.344715  | -0.39727  | -0.375    | -0.375392 |
| ('AL', 'WILCOX', 'm')               | -0.347835   | -0.352693  | -0.422544  | -0.486796 | -0.425302 | -0.375233 |
| ('WY', 'TETON', 'm')                |  0.137571   | -0.0746545 | -0.235213  | -0.118196 | -0.26871  | -0.372422 |
| ('GA', 'RICHMOND', 'l')             | -0.103028   | -0.137092  | -0.318379  | -0.338079 | -0.322492 | -0.37169  |
| ('DE', 'NEW CASTLE', 'l')           | -0.229827   | -0.219931  | -0.406213  | -0.340666 | -0.294957 | -0.370855 |
| ('ID', 'BLAINE', 'm')               | -0.0277148  | -0.192982  | -0.331851  | -0.201393 | -0.286833 | -0.367748 |
| ('OR', 'HOOD RIVER', 'm')           | -0.0410574  | -0.148392  | -0.308952  | -0.267229 | -0.296792 | -0.36738  |
| ('FL', 'GADSDEN', 'm')              | -0.33734    | -0.399161  | -0.389649  | -0.40624  | -0.374983 | -0.365626 |
| ('NY', 'WESTCHESTER', 'l')          | -0.211773   | -0.186298  | -0.276097  | -0.266803 | -0.336827 | -0.362688 |
| ('HI', 'HAWAII', 'l')               | -0.22847    | -0.226751  | -0.537286  | -0.511725 | -0.366257 | -0.362516 |
| ('MA', 'NORFOLK', 'l')              | -0.256693   | -0.216312  | -0.185361  | -0.152363 | -0.282375 | -0.360104 |
| ('VA', 'EMPORIA CITY', 's')         | -0.0855769  | -0.124719  | -0.307604  | -0.336424 | -0.313054 | -0.359899 |
| ('CA', 'MENDOCINO', 'm')            | -0.126765   | -0.299379  | -0.427879  | -0.386527 | -0.29861  | -0.357983 |
| ('NJ', 'UNION', 'l')                | -0.233129   | -0.181206  | -0.283929  | -0.340455 | -0.357247 | -0.356704 |
| ('MS', 'SHARKEY', 's')              | -0.217706   | -0.142162  | -0.370609  | -0.412717 | -0.359361 | -0.355932 |
| ('AZ', 'SANTA CRUZ', 'm')           | -0.212414   | -0.192064  | -0.313087  | -0.377933 | -0.474229 | -0.355083 |
| ('HI', 'MAUI', 'l')                 | -0.270281   | -0.223825  | -0.551719  | -0.502538 | -0.385677 | -0.354414 |
| ('ME', 'CUMBERLAND', 'l')           | -0.109802   | -0.152489  | -0.298701  | -0.269431 | -0.263488 | -0.353089 |
| ('TX', 'EL PASO', 'l')              | -0.181148   | -0.129036  | -0.325201  | -0.323655 | -0.431437 | -0.351649 |
| ('SD', 'HAAKON', 's')               |  0.685562   |  0.635484  |  0.659071  |  0.734432 |  0.822797 |  0.810026 |
| ('LA', 'LA SALLE', 'm')             |  0.5185     |  0.618788  |  0.723638  |  0.755021 |  0.796316 |  0.811078 |
| ('MT', 'CARTER', 's')               |  0.806202   |  0.771509  |  0.533487  |  0.732997 |  0.773537 |  0.811343 |
| ('GA', 'BRANTLEY', 'm')             |  0.382392   |  0.547348  |  0.631034  |  0.67061  |  0.785272 |  0.81229  |
| ('OK', 'ELLIS', 's')                |  0.519126   |  0.620192  |  0.704557  |  0.749028 |  0.796935 |  0.814736 |
| ('TX', 'JACK', 's')                 |  0.432078   |  0.584453  |  0.680781  |  0.783012 |  0.793731 |  0.816235 |
| ('OK', 'BEAVER', 's')               |  0.713762   |  0.768782  |  0.784903  |  0.788378 |  0.810076 |  0.816345 |
| ('AL', 'WINSTON', 'm')              |  0.399335   |  0.56548   |  0.632639  |  0.723286 |  0.81024  |  0.817175 |
| ('NE', 'LOGAN', 'xs')               |  0.669903   |  0.675991  |  0.591346  |  0.668213 |  0.812362 |  0.82     |
| ('TX', 'HANSFORD', 's')             |  0.802682   |  0.774569  |  0.76451   |  0.830275 |  0.800719 |  0.822179 |
| ('TX', 'OLDHAM', 's')               |  0.711886   |  0.7414    |  0.772826  |  0.827388 |  0.814346 |  0.828543 |
| ('LA', 'CAMERON', 's')              |  0.276835   |  0.392888  |  0.652094  |  0.761752 |  0.79442  |  0.82867  |
| ('TX', 'SHACKELFORD', 's')          |  0.595397   |  0.696136  |  0.71495   |  0.797506 |  0.847739 |  0.831695 |
| ('TX', 'STERLING', 's')             |  0.588771   |  0.769106  |  0.68336   |  0.866397 |  0.756714 |  0.834116 |
| ('NE', 'ARTHUR', 'xs')              |  0.768382   |  0.81203   |  0.676806  |  0.751908 |  0.831502 |  0.841549 |
| ('TX', 'LOVING', nan)               |  0.608974   |  0.6625    |  0.696203  |  0.703125 |  0.830769 |  0.848485 |
| ('TX', 'WHEELER', 's')              |  0.505651   |  0.643275  |  0.714477  |  0.773496 |  0.820902 |  0.851947 |
| ('OK', 'CIMARRON', 's')             |  0.675876   |  0.741935  |  0.760818  |  0.807853 |  0.826691 |  0.85389  |
| ('NE', 'MCPHERSON', 'xs')           |  0.651163   |  0.673077  |  0.665529  |  0.67354  |  0.84669  |  0.854305 |
| ('TX', 'MOTLEY', 's')               |  0.616822   |  0.659357  |  0.765993  |  0.805    |  0.855285 |  0.855828 |
| ('SD', 'HARDING', 's')              |  0.801642   |  0.748466  |  0.609418  |  0.752368 |  0.853247 |  0.859779 |
| ('NE', 'HAYES', 'xs')               |  0.735552   |  0.765886  |  0.679928  |  0.788497 |  0.859922 |  0.861423 |
| ('TX', 'ARMSTRONG', 's')            |  0.663113   |  0.657371  |  0.735354  |  0.780749 |  0.836435 |  0.863309 |
| ('TX', 'GLASSCOCK', 's')            |  0.856392   |  0.833021  |  0.807899  |  0.83391  |  0.859272 |  0.875957 |
| ('KS', 'WALLACE', 's')              |  0.736353   |  0.719178  |  0.738806  |  0.815789 |  0.845865 |  0.88     |
| ('NE', 'GRANT', 'xs')               |  0.714286   |  0.785354  |  0.754768  |  0.804408 |  0.85679  |  0.883085 |
| ('MT', 'GARFIELD', 's')             |  0.793011   |  0.821374  |  0.671252  |  0.794286 |  0.862117 |  0.889299 |
| ('TX', 'KING', 'xs')                |  0.773723   |  0.762821  |  0.877301  |  0.924138 |  0.90566  |  0.899371 |
| ('TX', 'BORDEN', 'xs')              |  0.626062   |  0.690808  |  0.764543  |  0.804408 |  0.819178 |  0.915865 |
| ('TX', 'ROBERTS', 'xs')             |  0.728597   |  0.81854   |  0.841699  |  0.856299 |  0.909747 |  0.930909 |


Observations:  many large urban counties that had strong shifts to the left (ie. 50%-80%) but most had been shifting left
over many years.

Also, many counties mostly in the Southeast that shifted right but those were much smaller generally and also had been
shifting right over time.  Did not see a sudden shift left or right looking at those trends over time.

From dataset [margin_shift_over_time.csv](/tabs/margin_shift_over_time.csv)

## Benford's analysis
To this point, I don't think I am seeing what I expected to see.   I'm seeing very consistent margin shifts to the left
and to the right that seems to be around the urban/rural divide. And this has consistently happened throughout elections
in this century.   

As I have read elsewhere, Benford's law is a useful tool that can be used as a red flag on certain types of datasets 
to indicate that the dataset is "unnatural."   The law holds that numbers in nature (population counts, rivers, observations, etc)
should follow a predictable pattern. When it doesn't, Benford's law flags that closer investigation should occur.

Also, there is debate about whether Benford's law applies to election results.  Much has been written about how it does not 
apply to precinct level data as the precinct is artificially constrained on its size by definition.  However, my analysis shows 
that US County Election results seem to conform to Benford's law very well.   This is true for most party results and for overall
total counts.  Benford's law does seem to break down on margins which are expressed in percentages.

Here are Benford's law calculations on the US Presidential Election Data since 2000. (2024 not year available). I'm using an error
calculation to show the mean absolute error from expected results.   

![benford](/img/benford_us_ele.jpg)

If there are any "red flags", they would be on the "OTHER" candidate in 2004, the Democrats in 2004, 2000, and the
Republicans in 2000.  Also, the Total count in 2008.  

But, the overall mean absolute error is very low in all cases significantly less than 1% (Benford expresses ratios of digits in 
percentages of total).  

So, this analysis to me doesn't raise red flags.

The 'worst' election result as measured by mean absolute error vs. Benford's Law expected in the broad sense is the DEMOCRAT vote
in 2004.   Plotting those first digit count frequencies vs. Benford's law expected shows very little error and is also 
convincing to me that Benford's Law applies to county level election data.

!['worst' broad result](/img/benford_error_worst.jpg)

As I was getting some "benford doesn't apply to elections" rants, I beg to differ.   Here are the plots of Benford Frequencies for all major parties and totals since 2000 (2024 to be added soon).  The mae is embeded in each facet and shows how low the absolute error is for the frequencies vs. Benford expected.  Hopefully this will put this little debate to rest.  I do agree that Benford doesn't seem to fit vote margins percentages as they are calculated vs. observed.  And it doesn't fit precinct level data as n is constrained by definition.   

![benford_facet](/img/benford_facet.jpg)

As I'm mostly focused on the question about where all the Biden votes came from in 2020, **_I do find it interesting_** that the highest error rates in 2020 vs. Benford are for Democrats (but while still relatively low). These errors look visually like they are on digits 4 and 5.  This would mean counties whose democrat votes have the first digit of 4 or 5 which I think means suburban metro counties or very small counties (40-59 votes * 10 to the power of 0-4).    Later, I'll dig into those counties and look at high zscores over 2016.

More to come ....

Raw results are in the [tabs](/tabs) as [benford_raw](/tabs/benford_raw.csv).







