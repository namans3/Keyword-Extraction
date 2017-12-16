#!/usr/bin/env python
# -*- coding: utf-8 -*-

#Import the necessary methods from tweepy library
import tweepy
import time
from textblob import TextBlob
import json
import sys

global location

#Variables that contains the user credentials to access Twitter API
access_token = "307949032-2jwo2hI1ZQB6WEkeqXHzi78bmmqiyeL6FTjYiQRz"
access_token_secret = "XqaiWQ7VEls2jmyApJUiCTA6fGb3lJZsFMJybG83WGFSF"
consumer_key = "qXqA2aSvW9C4DhkFfpOscaZ64"
consumer_secret = "aAoGjy0ABSo6rEpOrcBoLuIgZB746QRW9QVDvTU1JvAYcblPhC"

start_time = time.time() #grabs the system time


#This is a basic listener that just prints received tweets to stdout.This class 'Listener' is inherited from the StreamLister class
class Listener(tweepy.StreamListener):

    def __init__(self, start_time, time_limit=5):

        self.time = start_time
        self.limit = time_limit
        self.num_tweets_p = 0
        self.num_tweets_n = 0

    #on_data method of a stream listener receives all messages and calls functions according to the message type
    #the on_data method of Tweepy’s StreamListener conveniently passes data from statuses to the on_status method
    def on_data(self, data):
        all_data = json.loads(data)       
        if 'text' in all_data:
            if 'retweeted_status' in all_data:
                if 'extended_tweet' in all_data['retweeted_status']:
                    tweet = all_data["retweeted_status"]["extended_tweet"]["full_text"]
                else: tweet = all_data["text"]
            else:
                if 'extended_tweet' in all_data:
                        tweet = all_data["extended_tweet"]["full_text"]
                else:
                    tweet = all_data["text"]

            non_bmp_map = dict.fromkeys(range(0x10000, sys.maxunicode + 1), 0xfffd)
            tweet = (tweet.translate(non_bmp_map))
            tweet = tweet.replace('\n', ' ')
            print("Original Tweet: " , tweet)
            blob = TextBlob(tweet)
            txtblb = blob.sentiment
            print (txtblb.polarity, txtblb.subjectivity)
            print('\n')

            pos_filename = sys.path[0] + "\\Tweets\\" + location + "_p.txt"
            neg_filename = sys.path[0] + "\\Tweets\\" + location + "_n.txt"
            
            if (txtblb.polarity >= 0):
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
        #create an object of the Listner class which was inherited from the StreamListener class
        print("####################### Starting to listen to ", city)

        #This handles Twitter authetification and the connection to Twitter Streaming API
        #create an OAuthHandler instance
        auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
        auth.set_access_token(access_token, access_token_secret)
        api = tweepy.API(auth)
        stream = tweepy.streaming.Stream(auth, myStreamListener)
        stream.filter(track=[city], async = True, languages=["en"])
        time.sleep(1200)
        stream.disconnect()


if __name__ == '__main__':

    loc = open('locations.txt','r')
    MyListener = Listener("Tweet")
    for line in loc.readlines():
        location = line.rstrip('\n')
        Listener.TweetListener(True,MyListener,location)
