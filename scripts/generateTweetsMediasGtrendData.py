import json
import pandas as pd
import numpy as np

import pyspark
from pyspark import *
from pyspark.sql import *
from pyspark.sql.functions import *
from pyspark.sql import functions as F

# Get all tweets
countries = ['France', 'Italie', 'Allemagne', 'Suisse']
iso_countries = ['FR', 'IT', 'DE', 'CH']
spark = SparkSession.builder.getOrCreate()
all_tweets = spark.read.json("/mnt/datastore/data/coronavirus/*.json")

tweet_count = all_tweets.filter(col('geo_country').isin(iso_countries)).select(col('geo_country'), F.date_format('published','yyyy-MM-dd').alias('date')).groupby("date", 'geo_country').count().toPandas()
tweet_count['date'] = pd.to_datetime(tweet_count['date'])
tweet_count = tweet_count.sort_values(by=['date'], ascending=True)
tweet_count = tweet_count.rename(columns={"count": "Tweets"})

# Get Coronavirus Data
coronavirus = pd.read_csv("/mnt/datastore/data/coronavirus_2020-03-16.csv", sep=";")
coronavirus['date'] = pd.to_datetime(coronavirus['Date'])
coronavirus_count = coronavirus.groupby([coronavirus.Pays, coronavirus.date.dt.year, coronavirus.date.dt.month, coronavirus.date.dt.day])[['Infections', 'Guerisons', 'Deces']].sum()
coronavirus_count.index.names = ['Pays', 'Year', 'Month','Day']
coronavirus_count = coronavirus_count.reset_index()
coronavirus_count['date'] = pd.to_datetime(coronavirus_count[['Year', 'Month', 'Day']])
coronavirus_count = coronavirus_count[['date', 'Pays', 'Infections', 'Guerisons', 'Deces']]
coronavirus_count = coronavirus_count.sort_values(by=['date'], ascending=True)
coronavirus_merge = coronavirus_count[coronavirus_count['Pays'].isin(countries)]
coronavirus_merge.loc[coronavirus_merge['Pays']=='France','Pays'] = 'FR'
coronavirus_merge.loc[coronavirus_merge['Pays']=='Italie','Pays'] = 'IT'
coronavirus_merge.loc[coronavirus_merge['Pays']=='Allemagne','Pays'] = 'DE'
coronavirus_merge.loc[coronavirus_merge['Pays']=='Suisse','Pays'] = 'CH'

# Get Gtrend Data
interest = pd.read_csv('/mnt/datastore/data/gtrend_by_country.csv')
interest = interest[['date','Coronavirus', 'country']]
interest = interest[interest.country.isin(iso_countries)]
interest['date'] = pd.to_datetime(interest['date'])
interest = interest.rename(columns={"Coronavirus": "GTrend"})


# Get medias infos
allemagne = pd.read_csv('/mnt/datastore/data/medias/media_allemagne.csv', header=None)
france =  pd.read_csv('/mnt/datastore/data/medias/media_france.csv', header=None)
italy =  pd.read_csv('/mnt/datastore/data/medias/media_italy.csv', header=None)
suisse = pd.concat([pd.read_csv('/mnt/datastore/data/medias/media_suisse_fr.csv', header=None),
                   pd.read_csv('/mnt/datastore/data/medias/media_suisse_de.csv', header=None)])
suisse = suisse.groupby(0).sum().reset_index()

allemagne = allemagne.rename(columns={0: "date", 1:"Medias_DE"})
france = france.rename(columns={0: "date", 1:"Medias_FR"})
italy = italy.rename(columns={0: "date", 1:"Medias_IT"})
suisse = suisse.rename(columns={0: "date", 1:"Medias_CH"})

medias = allemagne.merge(france, how='inner', left_on=['date'], right_on=['date'])
medias = medias.merge(italy, how='inner', left_on=['date'], right_on=['date'])
medias = medias.merge(suisse, how='inner', left_on=['date'], right_on=['date'])

medias['date'] = pd.to_datetime(pd.to_datetime(medias['date']).dt.date)

# Merge Everything
all_together = coronavirus_merge.merge(interest, how='right', left_on=['date', 'Pays'], right_on=['date', 'country'])
all_together = all_together.merge(tweet_count, how='left', left_on=['date', 'country'], right_on=['date', 'geo_country'])
all_together['date'] = pd.to_datetime(all_together['date'])
all_together = all_together.sort_values(by=['date'])

all_together = all_together[['date', 'country', 'Infections', 'Guerisons', 'Deces', 'GTrend', 'Tweets']]
all_together = pd.pivot_table(all_together, values=['Infections', 'Deces', 'Guerisons', 'GTrend', 'Tweets'], index=['date'], columns=['country'])
    
all_together.columns = ['_'.join(col).strip() for col in all_together.columns.values]
all_together = all_together.reset_index()#.fillna(method='ffill').fillna(0)
all_together = all_together.merge(medias, how='right', left_on=['date'], right_on=['date'])

all_together = all_together.fillna(0)
all_together.to_csv("MediasVsGTrendsVsTweetsVsCorona.csv", index=False)
