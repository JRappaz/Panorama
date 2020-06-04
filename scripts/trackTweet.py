import tweepy
import networkx as nx
from networkx.readwrite import json_graph
import json
import pickle
import os
from urllib3.exceptions import ProtocolError
import twint
import time

tweet_id = '1257137118763253763'
DEPHT = 3

consumer_key        = "NEwDi3MGcErH7zrTuH8MdyJ4r"
consumer_secret     = "Je3GYOnSFMUGE5d8D4NKmO1r5YiAuEWs5dlYmRp8ZIsOW462DE"
access_token        = "312815721-6nPqECz4FO7uo5Jegw9DGm0i8VTRlkZ3DZTs7qxw"
access_token_secret = "sRDC1XuIjvwn6qIglPKj6nrZHxVu3B4Gz93O3I2LqzssT"

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth, wait_on_rate_limit=True)

def readGraph(filename):
    with open(filename) as f:
        js_graph = json.load(f)
    return json_graph.node_link_graph(js_graph)

def saveGraph(graph, filename):
    json_ = json_graph.node_link_data(graph)
    with open(filename, 'w') as outfile:
        json.dump(json_, outfile)

def addFollowers(graph, user_name, user_id):
    for page in tweepy.Cursor(api.followers, screen_name=tweet.user.screen_name).pages():
        for follower in page:
            graph.add_node(follower.id_str, name=follower.screen_name, followers=follower.followers_count, following=follower.friends_count)
            graph.add_edge(user_id, follower.id_str)
        time.sleep(60)

def followRetweets(graph, user_id, tweet_id, depht):
    tweets = api.retweets(tweet_id, count=100)
    print("depht: ", depht, " ; Number of retweets=", len(tweets))
    for i, tweet in enumerate(tweets):
        print(f"retweet: {i}/{len(tweets)}")
        rt_user_id = tweet.user.id_str
        rt_user_name = tweet.user.screen_name
        graph.add_node(rt_user_id, name=rt_user_name, followers=tweet.user.followers_count, following=tweet.user.friends_count, likes=tweet.favorite_count, retweets=tweet.retweet_count)
        graph.add_edge(user_id, rt_user_id)

        #addFollowers(graph, user_name, user_id)
        if(depht > 1):
            followRetweets(graph,rt_user_id, tweet.id, depht-1)


graph = nx.DiGraph()
tweet = api.get_status(tweet_id)
user_id = tweet.user.id_str
user_name = tweet.user.screen_name
graph.add_node(user_id, name=user_name, followers=tweet.user.followers_count, following=tweet.user.friends_count, likes=tweet.favorite_count, retweets=tweet.retweet_count)
#addFollowers(graph, user_name, user_id)
followRetweets(graph, user_id, tweet_id, depht=5)
#print(tweet.user.screen_name, tweet.user.id_str)
#print("likes:", tweet.favorite_count)
#print("retweets:", tweet.retweet_count)






saveGraph(graph, "test.json")


