#
# 1) Download data: https://www.ecdc.europa.eu/en/publications-data/download-todays-data-geographic-distribution-covid-19-cases-worldwide
# 2) Convert to csv
#

DATA_PATH = ""
OUTPUT_PATH = ""

# Read data from ecdc and convert date column to datetime
cor = pd.read_csv(DATA_PATH, sep=",")
cor['date'] = pd.to_datetime(cor['DateRep'], format="%d.%m.%y")
cor = cor.sort_values(by=['date'], ascending=True)

# Produce cumulative sum of number of cases
cor['cumsum_cases'] = cor.groupby('Countries and territories')['Cases'].transform(pd.Series.cumsum)
cor['cumsum_deaths'] = cor.groupby('Countries and territories')['Deaths'].transform(pd.Series.cumsum)

# Fix error in country code for United Kingdom
cor.loc[cor['GeoId']=='UK','GeoId'] = 'GB'

# Get List of countries in Europe (the continent)
all_countries = pd.read_csv("https://raw.githubusercontent.com/lukes/ISO-3166-Countries-with-Regional-Codes/master/all/all.csv")
europe_countries = all_countries[all_countries['region'] == 'Europe']

# Filter countries and add iso-code 3 to the dataset
cor_europe = cor[cor['GeoId'].isin(europe_countries['alpha-2'].values)]
cor_europe = cor_europe[['Countries and territories','GeoId','date','cumsum_cases','cumsum_deaths']]
cor_europe = cor_europe.rename(columns={'Countries and territories':'country', 'GeoId':'alpha-2'})
cor_europe['alpha-3'] = cor_europe['alpha-2'].apply(lambda x: europe_countries[europe_countries['alpha-2'] == x].head(1)['alpha-3'].values[0])

cor_europe.to_csv(OUTPUT_PATH)


