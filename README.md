# Keyword Extraction from Tweets
This is a python based program to get live stream of tweets filtered based on specific set of cities and classified into two sets i.e. positive and negative tweets. Each set is then analysed to extract top 10 keywords in the set.

# Requirements

Python 3.0 installed.
Install Tweepy: pip install tweepy
Twitter Account.

#Getting Twitter Data
To stream twitter data, we need 4 authentication keys.

Go to https://apps.twitter.com and click in 'Create New App' and fill in the requested information
After successfully creating an app, navigate to 'Keys and Access Tokens' section.
Generate Consumer Key and Consumer Secret and then create Access Token and Access Token Secret.

Now that we have the access credentials, we start with our tweet listener: TweetListener.py

# The code for TweetListener.py

from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream

#Variables that contains yours credentials to access Twitter API 
access_token = "YOUR_ACCESS_TOKEN"
access_token_secret = "YOUR_ACCESS_TOKEN_SECRET"
consumer_key = "YOUR_CONSUMER_KEY"
consumer_secret = "YOUR_CONSUMER_SECRET"
