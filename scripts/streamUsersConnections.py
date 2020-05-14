from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
import csv
import pickle
import os

OUTPUT_DIR = "/mnt/datastore/data/antivax/"
IDS_FILE = "seeds_ids.txt"
count = 0

users = []
with open(IDS_FILE, "rb") as fp:   # Unpickling
    users = pickle.load(fp)

class StdOutListener(StreamListener):
    def on_status(self, tweet):
        global count
        global users

        #if tweet.id not in users:
        #    return

        count += 1
        print("Number of tweets fetched: {}\r".format(count), end="")

        tweet_id = tweet.id_str
        user_id = tweet.user.id_str
        user_name = tweet.user.screen_name
        likes = tweet.favorite_count
        retweets = tweet.retweet_count
        text = tweet.text
        retweeted_from_user_id = None
        retweeted_from_user_name = None
        if hasattr(tweet, "retweeted_status"):  # Check if Retweet
            retweeted_from_user_id = tweet.retweeted_status.user.id_str
            retweeted_from_user_name = tweet.retweeted_status.user.screen_name
            try:
                text = tweet.retweeted_status.extended_tweet["full_text"]
            except AttributeError:
                test = tweet.retweeted_status.text
        else:
            try:
                text = tweet.extended_tweet["full_text"]
            except AttributeError:
                text = tweet.text

        created_at = tweet.created_at
        urls = tweet.entities['urls']
        followers = tweet.user.followers_count
        friends = tweet.user.friends_count
        user_location = tweet.user.location
        in_reply_to_user_id = tweet.in_reply_to_user_id
        in_reply_to_screen_name = tweet.in_reply_to_screen_name
        #user_mentions = tweet.entities['user_mentions']
        user_mentions_ids = [mention['id_str'] for mention in tweet.entities['user_mentions']]
        user_mentions_name = [mention['screen_name'] for mention in tweet.entities['user_mentions']]


        #print("tweet_id", tweet_id)
        #print("user_id", user_id)
        #print("user_name", user_name)
