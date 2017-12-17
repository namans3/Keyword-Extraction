# Keyword Extraction from Tweets
This is a python based program to get live stream of tweets filtered based on specific set of cities and classified into two sets i.e. positive and negative tweets. Each set is then analysed to extract top 10 keywords in the set.

# Requirements

- Python 3.0 installed.
- Install Tweepy: pip install tweepy
- Install Textblob: pip install Textbolb
- Instalal json: pip install json
- Install sys: pip install sys
- Install math: pip install math
- Install nltk: pip install nltk
- A Twitter Account.

# Creating Twitter App

To stream twitter data, we need 4 authentication keys and the following steps are to be followed.

Go to https://apps.twitter.com and click in 'Create New App' and fill in the requested information.

After successfully creating an app, navigate to 'Keys and Access Tokens' section.

Generate Consumer Key and Consumer Secret and then create Access Token and Access Token Secret.

Now that we have the access credentials, we start coding our tweet listener. Refer to TweetListener.py in the repository.

# Streaming Tweets using Twitter Streaming API

Refer to the file TweetListener.py

We start with importing the libraries that we would need. We use Tweepy for connecting to twitter and streamaing tweets. Since twitter API streams tweets as json objects, we use the json library to use finctions to extract the text of the tweet from the json object. Then we use textbolb to convert tweets into blobs (which is a list of words in the tweets) and doing sentiment analysis using the inbuilt functions. sys is quite useful for determining the file locations on a system.
```
import tweepy
import textblob from TextBlob
import json
import sys
```

declare a global variable 'location' that would capture the location name to be searched for when listening the tweets.
```
global location
```

Add the following variables that would contains your twitter app credentials to access Twitter API. Add the keys and tokens created above as shown below:
```
access_token = "YOUR_ACCESS_TOKEN"
access_token_secret = "YOUR_ACCESS_TOKEN_SECRET"
consumer_key = "YOUR_CONSUMER_KEY"
consumer_secret = "YOUR_CONSUMER_SECRET"
```

Now we build a listener that receives the tweets and classifies them into positive and negative and puts them in two different files. This class 'Listener' is inherited from the StreamLister class.
```
class Listener(tweepy.StreamListener):

    def __init__(self, start_time, time_limit=5):

        self.time = start_time
        self.limit = time_limit
        self.num_tweets_p = 0
        self.num_tweets_n = 0
```
Next, we read the data returend from Twitter API in JSON format. We load an entire json object into all_data.
Then we parse through it to identify if there exists an 'extended_tweet' as we the 'text' key contains the value which is a truncated form of tweet. Therefore, if we want to get the entire tweet, we go to the 'extended_tweet' key values. If extended_tweet key does not exist, it means that the text itself is complete.
```
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
```

Next comes the task to clean up the tweet so that it can be analysed and written into a file or printed on the terminal.Here we replace all emogis with � character as certaian emojies cause the file write operation to fail due to incompatible formats. We also remove newline characters.
```
            non_bmp_map = dict.fromkeys(range(0x10000, sys.maxunicode + 1), 0xfffd)
            tweet = (tweet.translate(non_bmp_map))
            tweet = tweet.replace('\n', ' ')
            print("Original Tweet: " , tweet)
```

Now we create a TextBlob of the tweet and use its inbuilt sentiment polarity score to seperat the tweets into two files 'location'_p.txt for positive or neutral tweets with polarity >= 0, and 'location'_n.txt for negative tweets with polarity < 0.  
```
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
            else:
                self.num_tweets_n += 1
                output=open(neg_filename,"a", encoding='utf-8')
                output.write(tweet)
                output.write('\n')
                output.close()
            
```

Now we create a function to access the twitter API for handling.This function receives an object of class Listener and the city name as parameters. We first create an oAuthHandler instance to handle twitter authentication and connection to Twitter Streaming API. Then we use the predefined Stream function in Tweepy to stream the tweets. We apply a filter based on the city and for language = en to capture only english tweets. After this, we set a sleep time of 1200s which can be varied. Tweets will keep stream during this sleep time and then the stream shall be disconnected.
```
    def TweetListener(self, myStreamListener, city):       
        #create an OAuthHandler instance
        #This handles Twitter authetification and the connection to Twitter Streaming API
        auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
        auth.set_access_token(access_token, access_token_secret)
        api = tweepy.API(auth)
        stream = tweepy.streaming.Stream(auth, myStreamListener)
        stream.filter(track=[city], async = True, languages=["en"])
        time.sleep(1200)
        stream.disconnect()
```

In the main function call, we read the locations file for list of locations and run TweetListener function one by one for all cities in the list. In a loop we We create an object of the Listener class. Then for every city in the location.txt file, we call the TweetListener function passing the object and the location name. This will run the function untill the sleep time is over and then the next location name will be read from the file and TweetListener start a new stream for that location. In this case, I have only done a single run through all locations but for practical purposes, this process could be set to repeat at a desired frequencty to keep the data up to date.
```
if __name__ == '__main__':
    loc = open('locations.txt','r')
    MyListener = Listener("Naman")
    for line in loc.readlines():
        location = line.rstrip('\n')
        Listener.TweetListener(True, MyListener, location)
```

# Keyword extraction of from Tweets using TF-IDF
TF-IDF, which stands for Term Frequency – Inverse Document Frequency, is a basic yet an effective method to extract keywords from text.
You can read more on wikipedia [here]. 

[here]: https://en.wikipedia.org/wiki/Tf%E2%80%93idf

In this project, we have used textblob to tokenize the words of tweets and we have developed functions to calculate TF and IDF scores based on which we rank all words and then extract the top 10 words in both  

Refer to the file TFIDFExtract.py in the repository. Code explaination is as below:

We import the following libraries:
```
import math #for calculations
from textblob import TextBlob #for word tokenisation
import time #for measurement of time
import re #used in cleaning tweets
import string #used in cleaning tweets
from nltk.corpus import stopwords #for removing stopwords from tweets
import sys #for reading system arguments
import json #writing the results into json file
```
### Reading the tweets from files

First we need to read the tweets from the files: <location>_p.txt and <location>_n.txt into seperate blobs of positive and negative tweets.

```
#Reading the positive tweets file <location>_p.txt
file=open((sys.path[0] + "\\Tweets\\" + location + "_p.txt"),"r", encoding='utf-8');
all_tweets=""
for line in file:
    all_tweets = all_tweets + " " + clean_tweet(line)
positiveblob = TextBlob(all_tweets)
file.close()

file=open((sys.path[0] + "\\Tweets\\" + location + "_n.txt"),"r", encoding='utf-8');
all_tweets=""
for line in file:
    all_tweets = all_tweets + " " + clean_tweet(line)
negativeblob = TextBlob(all_tweets)
file.close()
```
In the code above, we have used the clean_tweet function to clean up the tweet by removing generale english stopwords, punctuations, twitter specific text like RT for retweets, twitter handles and hyperlinks. 

```
def clean_tweet(tweet):

    #setting stop_word list
    punctuations = list(string.punctuation)
    stop_words = stopwords.words('english') + punctuations + ['RT', 'via', 'https', ':',"...","amp"] + location.lower().split()
    
    #Removing twitter handles which start with @
    tweet = ' '.join(word for word in tweet.split(' ') if not word.startswith('@'))

    #Removing words which are starating with ' (some words like 'nt etc end up in the blobs)
    tweet = ' '.join(word for word in tweet.split(' ') if not word.startswith("'"))
    
    "Removing hyperlinks
    tweet = ' '.join(word for word in tweet.split(' ') if not word.startswith('http'))
    
    #Convertig the tweet to lower text
    tweet = tweet.lower()
    
    #Extracting word tokes into TextBlob
    word_tokens = TextBlob(tweet)    
    
    #Reconstructing cleaned tweet
    cleaned_tweet = ""
    for word in word_tokens.words:
        if word not in stop_words and len(word) > 3:
            cleaned_tweet +=(' ' + word)

    return(cleaned_tweet)
```

Since we are using TF-IDF scoring, we will need a background collection of generic tweets so we can calculate a good IDF score for the words. Therefore, we are also reading a background collection file.

```
background = []
cleanedTweet=""
count= 1
with open('RandomCollection.txt',"r", encoding='utf-8') as f:
    for line in f:
        cleanedTweet = clean_tweet(line)
        background.append({"Tweet": count, "text": cleanedTweet, "blob": TextBlob(cleanedTweet)})
    count+=1
```

Now we define the functions to calculate TF-IDF. We begin with a function for calculating term frequency.
```
def tf(word, blob):
    return blob.words.count(word) / len(blob.words)
```

A document frequency function, which counts the number of tweets in the background collection which contain the word
```
def doc_freq(word, bloblist):
    return sum(1 for blob in bloblist if word in blob.words)
```

A function to calculate the inverse document frequency for a word based on the background collection of tweets
```
def idf(word, bloblist):
    return math.log(len(bloblist) / (1 + doc_freq(word, bloblist)))
```

Finally, a function to calculate the TF-IDF scores which basically just muluplies the TF and IDF scores and returns the product.
```
def tdidf(word, blob, bloblist):
    return tf(word, blob) * idf(word, bloblist)
```

We setup a function scorewords which would calculate the TF-IDF score through the functions described above for all the words in a blob (positiveblob or negativeblob) and then it sorts the words in decending order of magnitude of the score.
```
def scorewords(blob, blobs):
    scores = {word: tdidf(word, blob, blobs) for word in blob.words}
    return sorted(scores.items(), key=lambda x: x[1], reverse=True)
```

We write the keywords from positive and negative blobs into two seperate lists
```
positive_tweet_keywords=[]
word_scores = scorewords(positiveblob, [Tweet["blob"] for Tweet in background])
for word, score in word_scores[:10]:
        positive_tweet_keywords.append(word)
        
negative_tweet_keywords=[]
word_scores = scorewords(negativeblob, [Tweet["blob"] for Tweet in background])
for word, score in word_scores[:10]:
        negative_tweet_keywords.append(word)
        
```

Now we create a json object called "keywords" to write the positive and negative keyword lists as key:value pairs. Then we read the existing keywords.json file from the repositry and copy it to a json object called data. We add the newly calculated keywords for the location into the data object and then we write it back to the Keywords.json file. This file can then be consumed for any other application which needs to fetch the keywords for a given location.
```
keywords = {}
keywords["positive-tweets"] = positive_tweet_keywords
keywords["negative-tweets"] = negative_tweet_keywords

data = json.load(open(sys.path[0] + "\\Keywords.json"))

data[location] = keywords

with open((sys.path[0] + "\\Keywords.json"), 'w') as outfile:
    json.dump(data, outfile)
```

## Installation and execution
- To install, simply download the repository into a local folder in your machine.
- Ensure you have python installed
- Install all the needed libraries as indicated in the beginning.

