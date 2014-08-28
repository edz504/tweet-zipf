#!/usr/bin/env python
import twitter
import pandas as pd 
import numpy as np
import matplotlib.pyplot as plt
import pylab as pl
import nltk
import operator
from nltk.probability import FreqDist

import tweet_cleaner
import pickle
import ast
import datetime
from nltk.corpus import stopwords

#Setting up Twitter API
twitter_api = twitter.Api(
    consumer_key='qD0K86UokYrYbqhXa4I0NWQ4i',
    consumer_secret='RAttvgN9VUmnfYNwcA8SE96qpteuTm9uwsvLUGFLgsrFrn6QL9',
    access_token_key='431244726-M96XnETmwt7fZC3Dkbuy0jsUNOpFAjFZru4z4gCZ',
    access_token_secret='S4kbwMkUrZJfYmbsohaepnnbIMd1YfEZb4IaJoUQtDQ4a')

def getUserTweets(sn):
    user = twitter_api.GetUser(screen_name=sn)
    if (user.statuses_count < 1): # don't bother going through if we know
    # the user doesn't have any tweets
        return([])
    if (not user.protected):
        user_tweets = []
        keep_em_coming = True

        while (keep_em_coming):
            # for our first time, no max_id
            if len(user_tweets) == 0:
                this_user_tweets = twitter_api.GetUserTimeline(
                    screen_name=sn,
                    count=200)
            else:
                this_user_tweets = twitter_api.GetUserTimeline(
                    screen_name=sn,
                    count=200,
                    max_id=oldest_id)
            print 'Pulled in ' + str(len(this_user_tweets)) + ' new tweets'
            if len(this_user_tweets) <= 1:
                keep_em_coming = False
            else:
                oldest_id = min([t.id for t in this_user_tweets])
            user_tweets += this_user_tweets

        return(user_tweets)
    else: # return empty list for protected users
        return([])

# supply either a screen name, or a list of tweets
def getUserTweetWordFreqDist(sn, user_tweets=None):
    if user_tweets is None:
        user_tweets = getUserTweets(sn)
    user_tweets_str = [t.text.encode('utf-8') for t in user_tweets]
    user_tweets_clean1 = [tweet_cleaner.remove_sn(t_str1) for t_str1 in user_tweets_str]
    
    # bug here with specifics:
    # 'So funny! I want to listen to this again and again... ( http://t.co/Fwyw0He8)'
    user_tweets_clean2 = [tweet_cleaner.remove_urls(t_str2) for t_str2 in user_tweets_clean1]
    #

    user_tweets_clean3 = [tweet_cleaner.leave_alphanumeric(t_str3) for t_str3 in user_tweets_clean2]
    user_tweets_collapse = ''.join(user_tweets_clean3)
    user_tweets_tokens = nltk.word_tokenize(user_tweets_collapse)

    fdist = FreqDist(word.lower() for word in user_tweets_tokens)
    return(fdist)