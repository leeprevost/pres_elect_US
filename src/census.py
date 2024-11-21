import requests
import pandas as pd

county_est_2023_file = "https://www2.census.gov/programs-surveys/popest/datasets/2020-2023/counties/asrh/cc-est2023-alldata.csv"

saipe_file = "https://www2.census.gov/programs-surveys/saipe/datasets/2022/2022-state-and-county/est22all.xls"   #poverty and income

pop_est_2020_url = "https://www.ers.usda.gov/webdocs/DataFiles/48747/PopulationEstimates.xlsx?v=9655.3"

pop_est_2020 = pd.read_excel(pop_est_2020_url, skiprows=4, dtype={'FIPStxt': str}).rename(columns={"FIPStxt": 'county_fips'}).set_index('county_fips', drop=True)
#good source for 2024 reporting of state and county level results.
nyt_api = "https://static01.nyt.com/elections-assets/2020/data/api/2020-11-03/national-map-page/national/president.json"
r = requests.get(nyt_api)
nyt = r.json()

