import tweepy
import networkx as nx
from networkx.readwrite import json_graph
import json
import pickle
import os
from urllib3.exceptions import ProtocolError
import twint
import time
import csv

query               = 'chloroquine'
lang                = 'fr'
limit               = 2000000

GRAPH_FILENAME      = query + "_graph.json"
TWEETS_FILENAME     = query + "_tweets.csv"

consumer_key        = "NEwDi3MGcErH7zrTuH8MdyJ4r"
consumer_secret     = "Je3GYOnSFMUGE5d8D4NKmO1r5YiAuEWs5dlYmRp8ZIsOW462DE"
access_token        = "312815721-6nPqECz4FO7uo5Jegw9DGm0i8VTRlkZ3DZTs7qxw"
access_token_secret = "sRDC1XuIjvwn6qIglPKj6nrZHxVu3B4Gz93O3I2LqzssT"

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth, wait_on_rate_limit=True)

graph = nx.DiGraph()

header = ['tweet_id', 'user_id', 'user_name', 'followers', 'following', 'likes', 'retweets', 'date', 'reply_to_id', 'reply_to_username', 'user_mentions_ids', 'user_mentions_names', 'text', 'retweet_from_id', 'retweet_from_username', 'retweet_from_tweet_id']
with open(TWEETS_FILENAME, 'w') as f:
    writer = csv.writer(f)
    writer.writerow(header)

def saveGraph(graph, filename):
    json_ = json_graph.node_link_data(graph)
    with open(filename, 'w') as outfile:
        json.dump(json_, outfile)

def saveTweet(row, filename):
    with open(filename, 'a') as f:
        writer = csv.writer(f)
        writer.writerow(row)

def addConnection(graph, from_id, from_username, to_id, to_username):
        if graph.has_node(from_id):
            graph.nodes[from_id]['weight'] += 1
        else:
            graph.add_node(from_id, weight=1, name=from_username)
        
        # Add or update node interaction
        if graph.has_node(to_id):
            graph.nodes[to_id]['weight'] += 1
        else:
            graph.add_node(to_id, weight=1, name=to_username)
        
        # Add or update edge user - interaction
        if graph.has_edge(from_id, to_id):
            graph[from_id][to_id]['weight'] += 1
        else:
            graph.add_edge(from_id, to_id, weight=1)

def getRetweets(graph, user_id, tweet_id):
    tweets = api.retweets(tweet_id, count=100)
    for i, tweet in enumerate(tweets):
        rt_user_id = tweet.user.id_str
        rt_user_name = tweet.user.screen_name
        graph.add_node(rt_user_id, name=rt_user_name, followers=tweet.user.followers_count, following=tweet.user.friends_count, likes=tweet.favorite_count, retweets=tweet.retweet_count)
        graph.add_edge(user_id, rt_user_id)

counter = 0

for tweets in tweepy.Cursor(api.search, q=query,tweet_mode='extended', lang=lang).pages():
    for tweet in tweets:
        tweet_id = tweet.id_str
        user_id = tweet.user.id_str
        user_name = tweet.user.screen_name
        followers = tweet.user.followers_count
        following = tweet.user.friends_count
        likes = tweet.favorite_count
        retweets = tweet.retweet_count
        date = tweet.created_at
        reply_to_id = tweet.in_reply_to_user_id
        reply_to_username = tweet.in_reply_to_screen_name
        user_mentions_ids = [mention['id_str'] for mention in tweet.entities['user_mentions']]
        user_mentions_names = [mention['screen_name'] for mention in tweet.entities['user_mentions']]

        try:
            text = tweet.extended_tweet["full_text"]
        except AttributeError:
            text = tweet.full_text

        interactions = set()

        retweet_from_id = None
        retweet_from_username = None
        retweet_from_tweet_id = None
        # Add interaction if retweet
        if hasattr(tweet, "retweeted_status"):  
            interactions.add((tweet.retweeted_status.user.id_str, tweet.retweeted_status.user.screen_name))
            retweet_from_id = tweet.retweeted_status.user.id_str
            retweet_from_username = tweet.retweeted_status.user.screen_name
            retweet_from_tweet_id = tweet.retweeted_status.id_str

        # Add interaction if the tweet is a reply to another user
        interactions.add((tweet.in_reply_to_user_id, tweet.in_reply_to_screen_name))

        # Add interaction for each mention of another user in the tweet
        for mention in tweet.entities['user_mentions']:
            interactions.add((mention['id_str'], mention['screen_name']))

        # Discard None and interaction toward itself
        interactions.discard((None, None))
        interactions.discard((user_id, user_name))

        # Add interactions to the graph
        for interaction in interactions:
            addConnection(graph, user_id, user_name, interaction[0], interaction[1])


        row = [tweet_id, user_id, user_name, followers, following, likes, retweets, date, reply_to_id, reply_to_username, user_mentions_ids, user_mentions_names, text, retweet_from_id, retweet_from_username, retweet_from_tweet_id]
        saveTweet(row, TWEETS_FILENAME)

        counter += 1
        print(f"tweets fetched: {counter}/{limit}\r", end="")

    saveGraph(graph, GRAPH_FILENAME)
    
    


print("Total fetched : " + str(counter))


