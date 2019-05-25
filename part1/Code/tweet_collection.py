pip install tweepy

import tweepy
import csv
import pandas as pd

consumer_key ="**"
consumer_secret ="**"
access_token ="**"
access_token_secret ="**"

auth = tweepy.OAuthHandler(consumer_key, consumer_secret) 
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth,wait_on_rate_limit=True)

csvFile = open('dic_tweets.csv', 'a')

csvWriter = csv.writer(csvFile)

keywords = ['Trump','Democrats','Republican','Elections','President']

for key in keywords:
  
  for tweet in tweepy.Cursor(api.search,q=key,count=1000,
                             lang="en",
                             since="2019-01-01").items():
      if (not tweet.retweeted) and ('RT @' not in tweet.text):
        #print (tweet.created_at, tweet.text)
        csvWriter.writerow([tweet.created_at, tweet.text.encode('utf-8')])