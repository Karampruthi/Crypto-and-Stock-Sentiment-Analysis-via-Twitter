import time

import pandas as pd
from typing import List
import tweepy
from tweepy import OAuthHandler
from twitter_keys import *
from sqlalchemy import create_engine

import datetime
import psycopg2

# TWITTER
authorizer = OAuthHandler(api_key, api_key_secret)
authorizer.set_access_token(access_token, access_token_secret)
api = tweepy.API(authorizer)

# HEROKU DATABASE APP KARAMJOT
engine = create_engine(f'{dialect}://{user_name}:{password}@{host}:{port}/{db_name}')

NO_OF_TWEETS = 150


## getting tweets from twitter
def get_tweets(keyword: str) -> List[str]:
    all_tweets = []
    time = []
    for tweet in tweepy.Cursor(api.search_tweets, q=keyword + "-filter:retweets",
                               tweet_mode='extended', lang='en').items(NO_OF_TWEETS):
        all_tweets.append(tweet.full_text)
        time.append(tweet.created_at)
    all_tweets = pd.DataFrame(all_tweets, columns=['Tweet'])
    all_tweets['time'] = time

    return all_tweets


def Twitter():
    crypto_heroku = pd.read_sql('SELECT * FROM crypto_twitter', engine)

    df = pd.DataFrame()
    keywords = ['altcoin', 'crypto', 'cryptocurrency', 'nft', 'digital currency', 'blockchain', 'defi',
                'decentralized money']
    for i in keywords:
        df = df.append(get_tweets(i), ignore_index=True)

    df.drop_duplicates(inplace=True)

    list_index = []
    for n, i in enumerate(df.Tweet):
        if i in list(crypto_heroku.Tweet):
            list_index.append(n)

    df.drop(df.index[list_index], inplace=True)

    df.to_sql('crypto_twitter', engine, if_exists='append', index=False)


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    Twitter()
