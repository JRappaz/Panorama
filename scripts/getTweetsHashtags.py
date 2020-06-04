import pandas as pd
import twitter
from tld import get_tld
import pickle
import json
import os
import csv

#SEED_HASHTAGS = ['#sb277' ,  '#sb276' , '#icanVsCDC' , '#StopMandatoryVax', '#antivax']
SEED_HASHTAGS = ['vaccine']
OUTPUT_FILE = "antivax_2.csv"

consumer_key = "NEwDi3MGcErH7zrTuH8MdyJ4r"
consumer_secret = "Je3GYOnSFMUGE5d8D4NKmO1r5YiAuEWs5dlYmRp8ZIsOW462DE"
access_token = "312815721-6nPqECz4FO7uo5Jegw9DGm0i8VTRlkZ3DZTs7qxw"
access_token_secret = "sRDC1XuIjvwn6qIglPKj6nrZHxVu3B4Gz93O3I2LqzssT"


import tweepy

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth,wait_on_rate_limit=True)

count = 0

csvFile = open(OUTPUT_FILE, 'a')

#Use csv Writer
csvWriter = csv.writer(csvFile)


for tweet in tweepy.Cursor(api.search, q=" OR ".join(SEED_HASHTAGS), count=100, tweet_mode='extended').items():
    count += 1
    print("{} tweets fetched\r".format(count), end="")
    csvWriter.writerow([tweet.id, 
                        tweet.user.id,
                        tweet.user.screen_name,
                        tweet.favorite_count,
                        tweet.retweet_count,
                        tweet.full_text.encode('utf-8'),
                        tweet.created_at, 
                        tweet.entities['urls'],
                        tweet.user.followers_count,
                        tweet.user.location,
                        tweet.entities['hashtags']])

'''
def fetchTweets(results):
    min_id = results[0].id
    tweets = []
    for tweet in results:
        store = {}
        store['tweet_id'] = tweet.id
        store['user_id'] = tweet.user.id
        store['user_name'] = tweet.user.screen_name
        store['likes'] = tweet.favorite_count
        store['retweets'] = tweet.retweet_count
        store['text'] = tweet.full_text
        store['created_at'] = tweet.created_at
        store['urls'] = list(map(lambda x: x.expanded_url, tweet.urls))
        store['followers'] = tweet.user.followers_count
        store['friends'] = tweet.user.friends_count
        store['user_location'] = tweet.user.location
        store['hashtags'] = list(map(lambda x: x.text, tweet.hashtags))

        tweets.append(store)
    return tweets

with open(os.path.join(OUTPUT_DIR, "_min_" + str(min_id) + '.json'),'w') as fout:
        json.dump(tweets, fout)



results = api.GetSearch(term="#antivaccines", count=100, result_type="recent")
count = 0
while len(results) > 0 : 
    tweets, min_id = fetchTweets(results)
    count += len(results) 
    print("{} tweets fetched\r".format(count), end="")

    with open(os.path.join(OUTPUT_DIR, "_min_" + str(min_id) + '.json'),'w') as fout:
        json.dump(tweets, fout)

    results = api.GetSearch(term="#antivaccines",count=100,result_type="recent",max_id=min_id)
'''

print("\nTotal:", count)
