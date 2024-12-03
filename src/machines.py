import pandas as pd
from vote_data import fix_fips
from functools import partial
from utils import get_key

# https://github.com/trainingvirtue/2020-Election-Data-and-Analysis/tree/main
# trainingvirtue election analysis
# includes machine footprint data

""" Data desc
Index(['rucc2013', 'rucc1993', 'rucc2003', 'commuters2003', 'tot_pop2008',
       'tot_pop2012', 'tot_pop2016', 'tot_pop2019', 'stname', 'ctyname',
       'white2008', 'white2012', 'white2016', 'white2019', 'aa2019', 'aa2016',
       'aa2012', 'aa2008', 'hisp2019', 'hisp2016', 'hisp2012', 'hisp2008',
       'demvotes2000', 'repvotes2000', 'totalvotes2000', 'indvotes2000',
       'reptodem2000', 'indtotot2000', 'demvotes2004', 'repvotes2004',
       'totalvotes2004', 'indvotes2004', 'reptodem2004', 'indtotot2004',
       'demvotes2008', 'repvotes2008', 'totalvotes2008', 'indvotes2008',
       'reptodem2008', 'indtotot2008', 'demvotes2012', 'repvotes2012',
       'totalvotes2012', 'indvotes2012', 'reptodem2012', 'indtotot2012',
       'demvotes2016', 'repvotes2016', 'totalvotes2016', 'indvotes2016',
       'reptodem2016', 'indtotot2016', 'demvotes2020', 'repvotes2020',
       'totalvotes2020', 'indvotes2020', 'reptodem2020', 'indtotot2020',
       'state', 'state_po', 'county', 'turnout2020', 'turnout2016',
       'turnout2012', 'turnout2008', 'turnout2004', 'repoverdem2020',
       'repoverdem2016', 'repoverdem2012', 'repoverdem2008', 'repoverdem2004',
       'repoverdem2000', 'dominion', 'diebold', 'dominionvs', 'dss', 'swing',
       'swingdss', 'pred_2020', 'resid_2020'],
      dtype='object')"""

src_file = "https://raw.githubusercontent.com/trainingvirtue/2020-Election-Data-and-Analysis/refs/heads/main/election2020_pluscensus%20copy.csv"

def fetch_machines():
    el_data = []
    with pd.read_csv(src_file, chunksize=100000) as chunks:
        for chunk in chunks:
            el_data.append(chunk)

    el_data = pd.concat(el_data)
    el_data['fips'] = el_data.fips.apply(fix_fips)
    el_data.set_index('fips', drop=True, inplace=True)
    return el_data[machine_cols]

machine_cols = ['dominion', 'diebold', 'dominionvs', 'dss', 'swing',
                'swingdss']

get_machines = partial(get_key, key='machines', tfm=fetch_machines)