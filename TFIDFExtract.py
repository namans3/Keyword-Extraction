import math
from textblob import TextBlob
import time
import re
import string
from nltk.corpus import stopwords
import sys
import json

#Capture start time
start_time = time.time()

#Calculating term frequency
def tf(word, blob):
    return blob.words.count(word) / len(blob.words)

#Calculating document frequency i.e. which in this case means number of tweets of the background collection which contain the word
def doc_freq(word, bloblist):
    return sum(1 for blob in bloblist if word in blob.words)

#Calculating the Inverse Document Frequency
def idf(word, bloblist):
    return math.log(len(bloblist) / (1 + doc_freq(word, bloblist)))

#Calculating TF IDF = TF * IDF
def tdidf(word, blob, bloblist):
    return tf(word, blob) * idf(word, bloblist)

# Scoring each word based on TFIDF and sorting in descending order
def scorewords(blob, blobs):
    scores = {word: tdidf(word, blob, blobs) for word in blob.words}
    return sorted(scores.items(), key=lambda x: x[1], reverse=True)

#Function to clean tweets by removing stop words, punctuations and other keywords specific to tweets
def clean_tweet(tweet):

    #setting stop_word list
    punctuations = list(string.punctuation)
    stop_words = stopwords.words('english') + punctuations + ['RT', 'via', 'https', ':',"...","amp"] + location.lower().split()
    
    #Removing twitter handles which start with @
    tweet = ' '.join(word for word in tweet.split(' ') if not word.startswith('@'))
    
    #Removing words which are starating with ' (some words like 'nt etc end up in the blobs)
    tweet = ' '.join(word for word in tweet.split(' ') if not word.startswith("'"))
    
    #Removing hyperlinks
    tweet = ' '.join(word for word in tweet.split(' ') if not word.startswith('http'))
    
    #Convertig the tweet to lower case
    tweet = tweet.lower()
    
    #Extracting word tokes into TextBlob
    word_tokens = TextBlob(tweet)    
    
    #Reconstructing cleaned tweet
    cleaned_tweet = ""
    for word in word_tokens.words:
        if word not in stop_words and len(word) > 3:
            cleaned_tweet +=(' ' + word)

    return(cleaned_tweet)
    

#Starting by opening the list of locations "locations.txt" file and running the keyword extraction algorithm one by one per location and then the keywords are stored in Keywords.json file.

loc = open('locations.txt','r')
for line in loc.readlines():
    location = line.rstrip('\n')

    #Reading the positive tweets file <location>_p.txt and putting all words from all tweets in one blob.
    file=open(('Tweets\\' + location + '_p.txt'),'r', encoding='utf-8');
    all_tweets=""
    for line in file:
        all_tweets = all_tweets + " " + clean_tweet(line)
    positiveblob = TextBlob(all_tweets)
    file.close()

    #Reading the negative tweets file <location>_n.txt and putting all words from all tweets in one blob.
    file=open(('Tweets\\' + location + '_n.txt'),'r', encoding='utf-8');
    all_tweets=""
    for line in file:
        all_tweets = all_tweets + " " + clean_tweet(line)
    negativeblob = TextBlob(all_tweets)
    file.close()

    #Reading the background collection of tweets and  putting words of each tweet in different blobs stored in a list.
    background = []
    cleanedTweet=""
    count= 1
    with open('RandomCollection.txt','r', encoding='utf-8') as f:
        for line in f:
            cleanedTweet = clean_tweet(line)
            background.append({"Tweet": count, "text": cleanedTweet, "blob": TextBlob(cleanedTweet)})
        count+=1


    #Extract keywords from blob of words from positive tweets and add the top 10 scored words in a list.  
        positive_tweet_keywords=[]
    print("Keywords from positive tweets on : ", location, '\n') #printing is optional      
    word_scores = scorewords(positiveblob, [Tweet["blob"] for Tweet in background])
    for word, score in word_scores[:10]:
            print("\rWord: {}, TF-IDF: {}".format(word, round(score, 10))) #printing is optional
            positive_tweet_keywords.append(word)
    
    #Extract keywords from blob of words from negative tweets and add the top 10 scored words in a list.
    negative_tweet_keywords=[]
    print("Keywords from negative tweets on : ", location, '\n') #printing is optional
    word_scores = scorewords(negativeblob, [Tweet["blob"] for Tweet in background])
    for word, score in word_scores[:10]:
            print("\rWord: {}, TF-IDF: {}".format(word, round(score, 10))) #printing is optional
            negative_tweet_keywords.append(word)

    #Reading the end time and calculating elapsed time.
    end_time = time.time() - start_time
    print('Done. Elapsed: %d' % end_time) #printing is optional

    #Setting up a json object jeywords to capture list of keywords from positive and negative tweets
    keywords = {}
    keywords["positive-tweets"] = positive_tweet_keywords
    keywords["negative-tweets"] = negative_tweet_keywords

    #We load the existing Keywords.json file and add/update the keywords for the location 
    data = json.load(open('Keywords.json'))
    data[location] = keywords
    with open(('Keywords.json'), 'w') as outfile:
        json.dump(data, outfile)
