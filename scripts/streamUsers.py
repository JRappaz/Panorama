from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
import csv
import pickle
import os

OUTPUT_DIR = "/mnt/datastore/data/antivax/users_stream"
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
        #print("likes", likes)
        #print("retweets", retweets)
        #print("text", text)
        #print("created_at", created_at)
        #print("urls", urls)
        #print("followers", followers)
        #print("friends", friends)
        #print("user_location", user_location)
        #print("in_reply_to_user_id", in_reply_to_user_id)
        #print("in_reply_to_screen_name", in_reply_to_screen_name)
        #print("user_mentions", user_mentions)
        #print("retweeted_status", retweeted_status)

        new_row = {"tweet_id": tweet_id, "user_id":user_id, "user_name":user_name, "followers":followers, "friends":friends, "user_location":user_location, "likes":likes, 
                "retweets":retweets, "text":text, "created_at":created_at, "urls":urls, "in_reply_to_user_id":in_reply_to_user_id, "in_reply_to_screen_name":in_reply_to_screen_name, "user_mentions_ids":user_mentions_ids, "user_mentions_name": user_mentions_name, "retweeted_from_user_id" : retweeted_from_user_id, "retweeted_from_user_name": retweeted_from_user_name}

        with open(os.path.join(OUTPUT_DIR, "{}.csv".format(user_name)), 'a', newline='') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=new_row.keys())
            writer.writerow(new_row)

    def on_error(self, status_code):
        print("error", status_code)
        if status_code == 420:
            # returning non-False reconnects the stream, with backoff.
            return True

consumer_key        = "NEwDi3MGcErH7zrTuH8MdyJ4r"
consumer_secret     = "Je3GYOnSFMUGE5d8D4NKmO1r5YiAuEWs5dlYmRp8ZIsOW462DE"
access_token        = "312815721-6nPqECz4FO7uo5Jegw9DGm0i8VTRlkZ3DZTs7qxw"
access_token_secret = "sRDC1XuIjvwn6qIglPKj6nrZHxVu3B4Gz93O3I2LqzssT"

l = StdOutListener()
auth = OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
stream = Stream(auth, l, tweet_mode= 'extended')

print("Following {} users".format(len(users)))
stream.filter(follow=users)











