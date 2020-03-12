import pandas as pd
import twitter
from tld import get_tld
import pickle
import datetime

LIST_MEDIAS = ['nytimes', 'guardian', 'washingtonpost', 'MailOnline', 'USATODAY', 'letemps', 'lemondefr', '20minutesOnline']
medias_domains = ['nytimes.com', 'theguardian.com', 'washingtonpost.com', 'dailymail.co.uk', 'usatoday.com', 'letemps.ch', 'lemonde.fr', '20min.ch']
FROM_DATE = datetime.datetime.strptime('01/01/20 11:30:00', '%m/%d/%y %H:%M:%S').timestamp()

OUTPUT_PATH = "/mnt/datastore/data/all_tweets_medias.csv"

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
for media in LIST_MEDIAS:
    cnt = 0
    max_id = None
    fromDateReach = False
    while not fromDateReach:
        # Fetch tweets
        tweets = api.GetUserTimeline(screen_name=media, since_id=None, max_id=max_id, count=200, include_rts=False, trim_user=False, exclude_replies=True)
        if len(tweets) > 0:
            max_id = tweets[-1].id
        else:
            fromDateReach = True
            break

        # Get infos of each tweet
        for tweet in tweets[1:]:

            # Stop fetching if all tweet are retrieved 
            if datetime.datetime.strptime(tweet.created_at, '%a %b %d %H:%M:%S %z %Y').timestamp() < FROM_DATE:
                fromDateReach = True
                break

            cnt += 1
            print("Fetching ", cnt, " tweets, current date: ", tweet.created_at , "\r", end="")

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
                if res.fld in medias_domains:
                    article_url = url.expanded_url


            new_row = {"tweet_id": tweet_id, "user_id":user_id, "user_name":user_name, "followers":followers, "friends":friends, "user_location":user_location, "likes":likes,
                                                                                                                           "retweets":retweets, "text":text, "created_at":created_at, "url":article_url}

            tweets_df = tweets_df.append(new_row, ignore_index=True)

            tweets_df.to_csv(OUTPUT_PATH, index=False, mode='a', header=False)
            tweets_df.drop(tweets_df.index, inplace=True)




