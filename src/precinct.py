import pandas as pd

#precinct level data from MIT/harvard dataverse
#
prec_16_src = r"C:\Users\lee\Downloads\2016-precinct-president.csv"
prec_20_src = r"C:\Users\lee\Downloads\PRESIDENT_precinct_general.csv"

prec_16 = pd.read_csv(prec_16_src, encoding = 'latin-1', low_memory=False)
prec_20 = pd.read_csv(prec_20_src, encoding = 'latin-1', low_memory=False)

pt_20 =  prec_20.pivot_table(index = ['precinct'], columns = ['office', 'candidate'], values=['votes'], aggfunc = 'sum')