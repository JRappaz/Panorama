
import pandas as pd
from pytrends.request import TrendReq

APPEND_MODE = False
OUTPUT_PATH = "/mnt/datastore/data/gtrend_by_country.csv"
kw_list = ["Coronavirus"]
countries = ['FR', 'CH', 'US', 'DE', 'IT']
timeframe = 'today 3-m'

pytrends = TrendReq(hl='en-US', tz=360, retries=10, backoff_factor=0.5)

interest = pd.DataFrame(columns=['Coronavirus', 'isPartial', 'country'])

for country in countries:   
    pytrends.build_payload(kw_list, timeframe=timeframe, geo=country)
    interest_country = pytrends.interest_over_time()
    interest_country['country'] = country
    interest = interest.append(interest_country)
    
interest.index.name = 'date'    

if APPEND_MODE: 
    interest.to_csv('gtrend_by_country.csv', encoding='utf-8', mode='a', header=False)
else:
    interest.to_csv('gtrend_by_country.csv', encoding='utf-8')
