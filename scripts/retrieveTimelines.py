import pandas as pd
import twitter
from tld import get_tld
import pickle
import os
import numpy as np

PER_USER_LIMIT = 3200
PER_REQUEST_LIMIT = 200
LIST_ACCOUNT_PATH = "seeds.txt"
OUTPUT_DIR = "/mnt/datastore/data/antivax/timelines"

# List of all tweets IDs to be fetched
with open(LIST_ACCOUNT_PATH, "r") as fp:
  all_accounts = fp.readlines()

# Connect to the twitter API
api = twitter.Api(consumer_key="NEwDi3MGcErH7zrTuH8MdyJ4r",
                  consumer_secret="Je3GYOnSFMUGE5d8D4NKmO1r5YiAuEWs5dlYmRp8ZIsOW462DE",
                  access_token_key="312815721-6nPqECz4FO7uo5Jegw9DGm0i8VTRlkZ3DZTs7qxw",
                  access_token_secret="sRDC1XuIjvwn6qIglPKj6nrZHxVu3B4Gz93O3I2LqzssT",
                  tweet_mode="extended",
                  sleep_on_rate_limit=True)

for i, user_name in enumerate(all_accounts):
  user_name = user_name.strip()
  print("User : {} ({}/{})".format(user_name, i+1, len(all_accounts)))

  if os.path.exists(os.path.join(OUTPUT_DIR, "{}.csv".format(user_name))):
      print("Already fetch")
      continue

  # Create dataframe and prepare csv file to be filled, remove content and add the columns name
  tweets_df = pd.DataFrame(columns=["tweet_id", "user_id", "user_name","followers", "friends", "user_location", "likes", "retweets", "text", "created_at", "urls","in_reply_to_user_id", "in_reply_to_screen_name", "user_mentions", "retweeted_status"])
  tweets_df.to_csv(os.path.join(OUTPUT_DIR, "{}.csv".format(user_name)), index=False)

  steps = range(0,PER_USER_LIMIT, PER_REQUEST_LIMIT)
  count = 0
  max_id = None

  while True:
    # Fetch tweets
    try:
        tweets = api.GetUserTimeline(screen_name=user_name, max_id=max_id, count=200, include_rts=True, trim_user=False, exclude_replies=False)
    except Exception as e:
        print("Error with :", user_name)
        print(e)
        break
    count += len(tweets)

    print("Fetched {}\r".format(count), end="")

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
      in_reply_to_user_id = tweet.in_reply_to_user_id
      in_reply_to_screen_name = tweet.in_reply_to_screen_name
      user_mentions = tweet.user_mentions
      retweeted_status = tweet.retweeted_status

      new_row = {"tweet_id": tweet_id, "user_id":user_id, "user_name":user_name, "followers":followers, "friends":friends, "user_location":user_location, "likes":likes, 
              "retweets":retweets, "text":text, "created_at":created_at, "urls":urls, "in_reply_to_user_id": in_reply_to_user_id, "in_reply_to_screen_name":in_reply_to_screen_name, "user_mentions": user_mentions, "retweeted_status":retweeted_status}

      tweets_df = tweets_df.append(new_row, ignore_index=True)

    tweets_df.to_csv(os.path.join(OUTPUT_DIR, "{}.csv".format(user_name)), index=False, mode='a', header=False)
    max_id = tweets_df.tweet_id.min()
    tweets_df.drop(tweets_df.index, inplace=True)
    if len(tweets) <= 1:
      break

  try:
    user_name_timeline = pd.read_csv(os.path.join(OUTPUT_DIR, "{}.csv".format(user_name)))
    user_name_timeline = user_name_timeline.drop_duplicates(subset=['tweet_id'])
    print("\nFetched: {}".format(user_name_timeline.shape[0]))
    user_name_timeline.to_csv(os.path.join(OUTPUT_DIR, "{}.csv".format(user_name)), index=False)
  except Exception as e:
    print(e)





