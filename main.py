import pandas as pd
from typing import List
import tweepy
from tweepy import OAuthHandler
from twitter_keys import api_key, api_key_secret, access_token, access_token_secret
import re
from sqlalchemy import create_engine

import requests
import datetime
import psycopg2

## TWITTER
authorizer = OAuthHandler(api_key, api_key_secret)
authorizer.set_access_token(access_token, access_token_secret)
api = tweepy.API(authorizer)

## HEROKU DATABASE APP KARAMJOT
dialect = 'postgresql'
user_name = 'irdeevxiezwueq'
host = 'ec2-18-206-112-235.compute-1.amazonaws.com'
password = '3740500f5f053d042b6acb763311b14e8687df7bb9e623f4d4ae7b910004e3b3'
port = 5432
db_name = 'dbfkn8mi5ni7qc'
engine = create_engine(f'{dialect}://{user_name}:{password}@{host}:{port}/{db_name}')

## Reddit
CLIENT_ID = 'ribvRgMrTQZGDPpTfK-Bqg'
SECRET_KEY = 'iR7Q9HCVlnNX7-Z28bx7zJO2u_jlTg'

auth = requests.auth.HTTPBasicAuth(CLIENT_ID, SECRET_KEY)

data = {
    'grant_type': 'password',
    'username': 'LowAd9458',
    'password': 'capnid-7qegge-zogpoN'
}

headers = {'User-Agent': 'MyApi/0.0.1'}

res = requests.post('https://www.reddit.com/api/v1/access_token',
                    auth=auth, data=data, headers=headers)

TOKEN = res.json()["access_token"]

headers = {**headers, **{'Authorization': f'bearer {TOKEN}'}}

NO_OF_TWEETS = 25
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
    cryto_heroku = pd.read_sql('SELECT * FROM crypto_twitter', engine)

    df = pd.DataFrame()
    keywords = ['altcoin', 'crypto', 'cryptocurrency', 'nft', 'ethereum', 'bitcoin']
    for i in keywords:
        df = df.append(get_tweets(i), ignore_index=True)

    df.drop_duplicates(inplace=True)

    list_index = []
    for n, i in enumerate(df.Tweet):
        if i in list(cryto_heroku.Tweet):
            list_index.append(n)

    df.drop(df.index[list_index], inplace=True)

    df.to_sql('crypto_twitter', engine, if_exists='append', index=False)


def Reddit():
    crypto_reddit = pd.read_sql('SELECT * FROM crypto_reddit', engine)

    crypto = ['CryptoCurrency', 'CryptoMoonShots', 'CryptoMarkets', 'altcoin', 'NFT', 'Ethereum']
    nse = ['NSEbets']

    df = pd.DataFrame()
    for i in crypto:
        res = requests.get("https://oauth.reddit.com/r/" + i + "/new", headers=headers, params={'limit': '25'})

        for post in res.json()['data']['children']:
            df = df.append({
                'kind_id': post['kind'] + '_' + post['data']['id'],
                'subreddit': post['data']['subreddit'],
                'title': post['data']['title'],
                'selftext': post['data']['selftext'],
                'upvote_ratio': post['data']['upvote_ratio'],
                'ups': post['data']['ups'],
                'downs': post['data']['downs'],
                'score': post['data']['score'],
                'time': datetime.datetime.fromtimestamp(post['data']['created'])
            }, ignore_index=True)

    df.drop_duplicates(inplace=True)

    list_index = []
    for n, i in enumerate(df.title):
        if i in list(crypto_reddit.title):
            list_index.append(n)

    df.drop(df.index[list_index], inplace=True)

    df.to_sql('crypto_reddit', engine, if_exists='append', index=False)


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    Reddit()
    Twitter()
