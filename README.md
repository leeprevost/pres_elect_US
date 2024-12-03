# PRESIDENTIAL Election Anaylsis (2020-2024)
by: Lee Prevost, 11/7/2024

<!-- TOC -->
* [PRESIDENTIAL Election Anaylsis (2020-2024)](#presidential-election-anaylsis--2020-2024-)
  * [Methods:](#methods-)
  * [Vote Margins](#vote-margins)
  * [Bins:](#bins-)
  * [Distribution of Margins By County](#distribution-of-margins-by-county)
  * [Outliers - 2020 Vote](#outliers---2020-vote)
  * [Benford's analysis](#benfords-analysis)
* [Closer Analysis of Benford at Digit Level](#closer-analysis-of-benford-at-digit-level)
<!-- TOC -->



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

Here are Benford's law calculations on the US Presidential Election Data since 2000. (2024 not yet available). I'm using an error
calculation to show the mean absolute percent error from expected results meaning the mean percentage deviation of digit counts from expected.   

![benford](/img/benford_us_ele.jpg)

My first take from this is that:
1) County election results are following Benford's Law very well.
2) The mean percent error for each election looks fairly low with 'normal' noise due to the human process of counting votes.

Even the worst broad result seems to conform to Benford fairly well.

!['worst' broad result](/img/benford_error_worst.jpg)

As I was getting some "benford doesn't apply to elections" rants, I beg to differ.   Here are the plots of Benford Frequencies for all major parties and totals since 2000 (2024 to be added soon).  The mae is embeded in each facet and shows how low the absolute error is for the frequencies vs. Benford expected.  Hopefully this will put this little debate to rest.  I do agree that Benford doesn't seem to fit vote margins percentages as they are calculated vs. observed.  And it doesn't fit precinct level data as n is constrained by definition.

![benford_facet](/img/benford_facet.jpg)







