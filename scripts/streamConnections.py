from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
import networkx as nx
from networkx.readwrite import json_graph
import json
import pickle
import os
from urllib3.exceptions import ProtocolError


OUTPUT_FILE = "graph.json"
IDS_FILE = "seeds_ids_filtered.txt"
APPEND = True

def readGraph():
    with open(OUTPUT_FILE) as f:
        js_graph = json.load(f)
    return json_graph.node_link_graph(js_graph)

class StdOutListener(StreamListener):
    count = 0

    if APPEND:
        graph = readGraph()
    else:
        graph = nx.DiGraph()

    def saveGraph(self):
        json_ = json_graph.node_link_data(self.graph)
        with open(OUTPUT_FILE, 'w') as outfile:
            json.dump(json_, outfile)

    def addConnection(self, from_id, from_username, to_id, to_username):

        if self.graph.has_node(from_id):
            self.graph.nodes[from_id]['weight'] += 1
        else:
            self.graph.add_node(from_id, weight=1, name=from_username)
        
        # Add or update node interaction
        if self.graph.has_node(to_id):
            self.graph.nodes[to_id]['weight'] += 1
        else:
            self.graph.add_node(to_id, weight=1, name=to_username)
        
        # Add or update edge user - interaction
        if self.graph.has_edge(from_id, to_id):
            self.graph[from_id][to_id]['weight'] += 1
        else:
            self.graph.add_edge(from_id, to_id, weight=1)

    def on_status(self, tweet):
        self.count += 1
        print("Number of tweets fetched: {} ; Number of nodes: {} ; Number of edges: {}\r".format(self.count, self.graph.number_of_nodes(), self.graph.number_of_edges()), end="")

        user_id = tweet.user.id_str
        user_name = tweet.user.screen_name

        interactions = set()

        # Add interaction if retweet
        if hasattr(tweet, "retweeted_status"):  
            interactions.add((tweet.retweeted_status.user.id_str, tweet.retweeted_status.user.screen_name))

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
            self.addConnection(user_id, user_name, interaction[0], interaction[1])

        # Save graph periodically
        if(self.count%100 == 0):
            self.saveGraph()


    def on_error(self, status_code):
        print("error", status_code)
        if status_code == 420:
            # returning non-False reconnects the stream, with backoff.
            return True

consumer_key        = "NEwDi3MGcErH7zrTuH8MdyJ4r"
consumer_secret     = "Je3GYOnSFMUGE5d8D4NKmO1r5YiAuEWs5dlYmRp8ZIsOW462DE"
access_token        = "312815721-6nPqECz4FO7uo5Jegw9DGm0i8VTRlkZ3DZTs7qxw"
access_token_secret = "sRDC1XuIjvwn6qIglPKj6nrZHxVu3B4Gz93O3I2LqzssT"

users = []
with open(IDS_FILE, "rb") as fp:   # Unpickling
    users = pickle.load(fp)

l = StdOutListener()
auth = OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
stream = Stream(auth, l, tweet_mode= 'extended')

print("Following {} users".format(len(users)))
while True:
    try:
        stream.filter(follow=users, languages=["fr"])
    except (ProtocolError, AttributeError):
        print("\nProtocol or Attribute Error")
        continue
