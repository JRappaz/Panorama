import pandas as pd
import twitter
from tld import get_tld
import pickle

API_GET_LIMIT = 1

LIST_MEDIAS_PATH = "/mnt/datastore/data/handle_store.csv"
TWEETS_IDS_PATH = "/mnt/datastore/data/media_tweets_ids.txt"
OUTPUT_PATH = "/mnt/datastore/data/tweets_medias_full.csv"

# List of all tweets IDs to be fetched
with open(TWEETS_IDS_PATH, "rb") as fp:
  all_tweets_ids = pickle.load(fp)

NB_TWEETS = len(all_tweets_ids)

# List of known medias domains, to filter urls
medias_accounts = pd.read_csv(LIST_MEDIAS_PATH, header=None)

# Connect to the twitter API
api = twitter.Api(consumer_key="QfjQAyXBjSeyYKiUFg1P2vXgV",
                  consumer_secret="Db1sT2E0UbXVnKSDU7S6ADMD6d2L3zON1flTIEFTkhu5Zel5fe",
                  access_token_key="312815721-HNwjAnqvua8mPg6UBLd0Jy8BNsS3ZJSaWkOhsKPp",
                  access_token_secret="LIxHsOZugHibFMSr87dK9BEUKymhdeFeOgPXwZVPzWjJX",
                  tweet_mode="extended",
                  sleep_on_rate_limit=True)

# Create dataframe and prepare csv file to be filled, remove content and add the columns name
tweets_df = pd.DataFrame(columns=["tweet_id", "user_id", "user_name","followers", "friends", "user_location", "likes", "retweets", "text", "created_at", "url"])
tweets_df.to_csv(OUTPUT_PATH, index=False)

for i in range(NB_TWEETS//API_GET_LIMIT + 1):
  print("Fetching ", i*API_GET_LIMIT, "/", NB_TWEETS, "\r", end="")

  # Take the next group of tweet to extract
  tweets_ids = all_tweets_ids[:API_GET_LIMIT]

  # Remove them from all tweets
  all_tweets_ids = all_tweets_ids[API_GET_LIMIT:]

  # Fetch tweets
  tweets = api.GetStatuses(tweets_ids)

  # Get infos of each tweet
  for tweet in tweets:
    tweet_id = tweet.id
    user_id = tweet.user.id
    user_name = tweet.user.screen_name
    likes = tweet.favorite_count
    retweets = tweet.retweet_count
    text = tweet.full_text
    created_at = tweet.created_at
    urls = tweet.urls
    followers = tweet.user.followers_count
    friends = tweet.user.friends_count
    user_location = tweet.user.location

    # Fetch URL if from known newspaper domain
    article_url=None
    for url in urls:
      res = get_tld(url.expanded_url, as_object=True)
      if res.fld in medias_accounts[0].values:
        article_url = url.expanded_url

    new_row = {"tweet_id": tweet_id, "user_id":user_id, "user_name":user_name, "followers":followers, "friends":friends, "user_location":user_location, "likes":likes, 
              "retweets":retweets, "text":text, "created_at":created_at, "url":article_url}

    tweets_df = tweets_df.append(new_row, ignore_index=True)

  tweets_df.to_csv(OUTPUT_PATH, index=False, mode='a', header=False)
  tweets_df.drop(tweets_df.index, inplace=True)




