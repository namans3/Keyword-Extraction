#!/usr/bin/env python
# -*- coding: utf-8 -*-

import tweepy
import time
from textblob import TextBlob
import json
import sys

#Declaring a global variable to store the location name which would be used for accessing the location files
global location

#Variables that contains the user credentials to access Twitter API. (Please specify your credentials below as indicated)
access_token = "307949032-2jwo2hI1ZQB6WEkeqXHzi78bmmqiyeL6FTjYiQRz"
access_token_secret = "XqaiWQ7VEls2jmyApJUiCTA6fGb3lJZsFMJybG83WGFSF"
consumer_key = "qXqA2aSvW9C4DhkFfpOscaZ64"
consumer_secret = "aAoGjy0ABSo6rEpOrcBoLuIgZB746QRW9QVDvTU1JvAYcblPhC"


#This is a basic listener that streams tweets and writes them into files. This class 'Listener' is inherited from the StreamListener class
class Listener(tweepy.StreamListener):

    def __init__(self):
        self.num_tweets_p = 0
        self.num_tweets_n = 0

    #on_data method of Tweepy’s StreamListener receives all messages and calls functions according to the message type
    #the on_data method of Tweepy’s StreamListener conveniently passes data from statuses to the on_status method
    def on_data(self, data):
        all_data = json.loads(data)       

        #Checking if "text" key is present in the json object received by the stream
        if 'text' in all_data:
            #Checking if it is a retweet or an original tweet. Retweets have the retweeted_status key.
            if 'retweeted_status' in all_data:
                #Checking if the tweet has extended_tweet key. It means that the text key contains truncated content, and
                #therefore we go for the content of the full_text key under extended_tweet. Otherwise, we take the value of
                #text key.
                if 'extended_tweet' in all_data['retweeted_status']:
                    tweet = all_data["retweeted_status"]["extended_tweet"]["full_text"]
                else: tweet = all_data["text"]
            else:
                if 'extended_tweet' in all_data:
                        tweet = all_data["extended_tweet"]["full_text"]
                else:
                    tweet = all_data["text"]

            #Removing all emoji characters as they can cause issue in saving the file
            non_bmp_map = dict.fromkeys(range(0x10000, sys.maxunicode + 1), 0xfffd)
            tweet = (tweet.translate(non_bmp_map))
            tweet = tweet.replace('\n', ' ')
            print(tweet)

            #Creating a blob using TextBlob which tokenizes the words of the tweet. We then use the sentiment function of
            #TextBlob to identify the sentiment polarity.
            blob = TextBlob(tweet)
            txtblb = blob.sentiment
            print (txtblb.polarity, txtblb.subjectivity, '\n')

            #Setting names of two file for positive and negative tweets
            pos_filename = sys.path[0] + "\\Tweets\\" + location + "_p.txt"
            neg_filename = sys.path[0] + "\\Tweets\\" + location + "_n.txt"
            
            #When polarity is positive, then we write it to the positive file else we write it to the negative file.
            if (txtblb.polarity > 0):
                self.num_tweets_p += 1
                output=open(pos_filename,"a", encoding='utf-8')
                output.write(tweet)
                output.write('\n') 
                output.close()
                #return True
            else:
                self.num_tweets_n += 1
                output=open(neg_filename,"a", encoding='utf-8')
                output.write(tweet)
                output.write('\n')
                output.close()
                #return True

            #When number of positive and negative tweets grows over 500 then we stop listening.    
            if self.num_tweets_p < 500 or self.num_tweets_n < 500:
                return True
            else:
                return False

    def on_status(self, status):
        print (status.text)

        
    # We can use on_error to catch 420 errors and disconnect our stream.
    def on_error(self, status):
        if status == 420:
            return False
        print (status)


    def TweetListener(self, myStreamListener, city):

        print("Listen to tweets for ", city, "...")
        #This handles Twitter authentication and the connection to Twitter Streaming API
        #create an OAuthHandler instance
        auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
        auth.set_access_token(access_token, access_token_secret)
        api = tweepy.API(auth)
        stream = tweepy.streaming.Stream(auth, myStreamListener)

        #In the filter function we can specify the words we would like to filter the tweets by using track=[parameters] 
        #and also specify tweet language
        #Filtering can also be done by providing geo coordinates of a location and using location based filtering. 
        #In this case, we use city name based filter
        stream.filter(track=[city], async = True, languages=["en"])

        #Set the time limit of listening tweets for each location in the location.txt file here.
        time.sleep(1200)
        stream.disconnect()


if __name__ == '__main__':

    loc = open('locations.txt','r')
    #create an object of the Listner class which was inherited from the StreamListener class
    MyListener = Listener()

    #For every location in location.txt file, we will listen to the tweets which will be recorded in files in Tweets folder
    for line in loc.readlines():
        location = line.rstrip('\n')
        Listener.TweetListener(True,MyListener,location)
