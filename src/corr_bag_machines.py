import utils
import pandas as pd
import src

keys = ['fips_key', 'machines', 'anom_20_dem_votes']

for key in keys:
    locals()[key] = pd.read_hdf(src.CACHE, key)

machines = machines.assign(bag = False)
machines.loc[machines.index.isin(bag.index), 'bag'] = True

corr = machines.corr()