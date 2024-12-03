import requests
import pandas as pd
from functools import partial
from utils import get_key


county_est_2023_file = "https://www2.census.gov/programs-surveys/popest/datasets/2020-2023/counties/asrh/cc-est2023-alldata.csv"

saipe_file = "https://www2.census.gov/programs-surveys/saipe/datasets/2022/2022-state-and-county/est22all.xls"   #poverty and income

pop_est_2020_url = "https://www.ers.usda.gov/webdocs/DataFiles/48747/PopulationEstimates.xlsx?v=9655.3"

pop_est_2020 = pd.read_excel(pop_est_2020_url, skiprows=4, dtype={'FIPStxt': str}).rename(columns={"FIPStxt": 'county_fips'}).set_index('county_fips', drop=True)
#good source for 2024 reporting of state and county level results.
nyt_api = "https://static01.nyt.com/elections-assets/2020/data/api/2020-11-03/national-map-page/national/president.json"
r = requests.get(nyt_api)
nyt = r.json()

# cancer single age by county over years
# https://seer.cancer.gov/popdata/popdic.html
#seer = pd.read_fwf(seer_url, compression='gzip', encoding='latin-1')
seer_local = r"C:\Users\lee\Downloads\us.1990_2022.singleages.adjusted.txt"
seer_url = "https://seer.cancer.gov/popdata/yr1990_2022.19ages/us.1990_2022.19ages.adjusted.txt.gz"

col_specs = pd.read_html("https://seer.cancer.gov/popdata/popdic.html")[0]
col_names = col_specs.iloc[:, 0].str.split(" ").apply(lambda x: x[0])
col_names[2] = 'state_fips'
col_specs = col_specs.assign(col_names = col_names)



def _transform_seer(chunk):
    chunk.columns = col_specs.col_names
    chunk.attrs.update(description = col_specs.iloc[:, 0].to_list())
    chunk = chunk.assign(fips = chunk.iloc[:, 2].astype(str).str.zfill(2) + chunk.iloc[:, 3].astype(str).str.zfill(3))
    chunk = chunk.set_index('fips', drop=True)
    return chunk
def transform_seer():
    with pd.read_fwf(seer_url, compression='gzip', widths=col_specs.Length.to_list(), header=None, chunksize=1000000) as chunks:
        # first chunk, write over, then append
        mode = 'w'
        append=False
        for chunk in chunks:
            chunk = _transform_seer(chunk)
            chunk.to_hdf(db, key="seer", format='table', mode=mode, append=append)
            append=True
            mode = 'a'


# first 3 - too young.  4, partial, rest, full
vap_wt = pd.Series([0.0,0.0,0.0,0.40] + [1.0]*(19-4), name="vap_wt")



race = {
    1: "White",
    2: "Black",
    3: "American Indian, Alaska Native",
    4: "Asian or Pacific Islander"
}

race_short = dict(zip(race.keys(), ['W', "B", "AI_AN", "A_PI"]))

origin = {
    0: "Non-Hispanic",
    1: "Hispanic",
    9: "NA"
}

sex = {1: "M", 2: "F"}
origin_short = dict(zip(origin.keys(), ["NH", "H", "NA"]))



def seer_sum():
    seer = get_key('seer', transform_seer).reset_index()
    pop_wt = seer.Age.replace(vap_wt) * seer.Population
    seer = seer.assign(VAPWtPop = pop_wt)
    seer.Origin = seer.Origin.replace(origin_short)
    seer.Race = seer.Race.replace(race_short)
    seer.Sex = seer.Sex.replace(sex)
    pt = seer.pivot_table(index=['Year', 'fips'], columns = ["Race", "Origin", "Sex"], values=["VAPWtPop", "Population"], aggfunc='sum')
    return pt

get_seer_sum = partial(get_key, key="seer_sum", tfm=seer_sum)

def ratio_seer_sum():
    seer_sum = get_seer_sum()
    g = seer_sum.T.groupby(level=[0,1])
    g2 = seer_sum.T.groupby(level=[0,2])
    g3 = seer_sum.T.groupby(level=[0,3])
    new = pd.concat(
        [
            (g.sum()).T,
            (g2.sum()).T,
            (g3.sum()).T
        ], axis=1).sort_index(axis=1)
    new = new.stack(0, future_stack=True)
    tot = new["M"] + new["F"]
    return new.div(tot, axis=0).drop(["M", "NH", "W"], axis=1)

def total():
    seer_sum = get_seer_sum()
    g3 = seer_sum.T.groupby(level=[0,3])
    return g3.sum().groupby(level=0).sum().T


get_seer_ratio = partial(get_key, key='seer_ratio', tfm=ratio_seer_sum)
get_total = partial(get_key, key='seer_total', tfm=total)



