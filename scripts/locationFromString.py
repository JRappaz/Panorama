import pandas as pd
from geopy.geocoders import Nominatim
from geopy.extra.rate_limiter import RateLimiter
from tqdm import tqdm

INPUT_PATH = "/mnt/datastore/data/tweets_medias_full.csv"
OUTPUT_PATH = "/mnt/datastore/data/tweets_medias_full_v2.csv"
tqdm.pandas()


dataset = pd.read_csv(INPUT_PATH)
dataset = dataset[~dataset.text.isna()]
geolocator = Nominatim(user_agent="appName")

geocode = RateLimiter(geolocator.geocode, min_delay_seconds=0.5)
dataset['location'] = dataset['user_location'].progress_apply(geocode)

dataset.to_csv(OUTPUT_PATH, encoding='utf-8', index=False)

