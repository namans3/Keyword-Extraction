# Keyword Extraction from Tweets
This is a python based program to get live stream of tweets filtered based on specific set of cities and classified into two sets i.e. positive and negative tweets. Each set is then analysed to extract top 10 keywords in the set.

# Requirements

Python 3.0 installed.
Install Tweepy: pip install tweepy
Install Textblob: pip install Textbolb
Instalal json: pip install json
Install sys: pip install sys
Twitter Account.

#Creating Twitter App
To stream twitter data, we need 4 authentication keys and the following steps are to be followed.

Go to https://apps.twitter.com and click in 'Create New App' and fill in the requested information.

After successfully creating an app, navigate to 'Keys and Access Tokens' section.

Generate Consumer Key and Consumer Secret and then create Access Token and Access Token Secret.

Now that we have the access credentials, we start with our tweet listener: TweetListener.py

# Connecting to Twitter Streaming API

Import the libraries
```
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
```

declare a global variable 'location' that would capture the city name.
```
global location
```

Add the following variables that would contains yours credentials to access Twitter API. Add the tokens created here as shown below: 
```
access_token = "YOUR_ACCESS_TOKEN"
access_token_secret = "YOUR_ACCESS_TOKEN_SECRET"
consumer_key = "YOUR_CONSUMER_KEY"
consumer_secret = "YOUR_CONSUMER_SECRET"
```
```
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

            pos_filename = sys.path[0] + "\\Data\\" + location + "_p.txt"
            neg_filename = sys.path[0] + "\\Data\\" + location + "_n.txt"
            
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


    def TweetListener(self, city):
        #create an object of the Listner class which was inherited from the StreamListener class
        myStreamListener = Listener("Ropa")

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
    for line in loc.readlines():
        MyListener = Listener("Naman")
        location = line.rstrip('\n')
        Listener.TweetListener(True,location)
```

