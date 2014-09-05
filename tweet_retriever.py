#!/usr/bin/env python
import twitter
import pandas as pd 
import numpy as np
import matplotlib.pyplot as plt
import pylab as pl
import nltk
import operator
from nltk.probability import FreqDist

from tweet_cleaner import remove_sn, remove_urls, leave_alphanumeric
import pickle
import ast
import datetime
from nltk.corpus import stopwords

#Setting up Twitter API
mine = [s.strip() for s in open('twitter_api.txt', 'rb').readlines()]
twitter_api = twitter.Api(
    consumer_key=mine[0],
    consumer_secret=mine[1],
    access_token_key=mine[2],
    access_token_secret=mine[3])

def getUserTweets(u):
    if (u.statuses_count < 1 or u.protected): # don't bother going through if we know the user doesn't have any tweets
        # or if they're protected
        return([])
    else (not u.protected):
        user_tweets = []
        keep_em_coming = True

        while (keep_em_coming):
            # for our first time, no max_id
            if len(user_tweets) == 0:
                this_user_tweets = twitter_api.GetUserTimeline(
                    screen_name=u.screen_name,
                    count=200)
            else:
                this_user_tweets = twitter_api.GetUserTimeline(
                    screen_name=u.screen_name,
                    count=200,
                    max_id=oldest_id)
            # print 'Pulled in ' + str(len(this_user_tweets)) + ' new tweets'
            print '.'
            if len(this_user_tweets) <= 1:
                keep_em_coming = False
            else:
                oldest_id = min([t.id for t in this_user_tweets])
            user_tweets += this_user_tweets

        return(user_tweets)


# supply either a screen name, or a list of tweets
def getUserTweetWordFreqDist(u, user_tweets=None):
    if user_tweets is None:
        user_tweets = getUserTweets(u)
    user_tweets_str = [t.text.encode('utf-8') for t in user_tweets]
    user_tweets_clean1 = [tweet_cleaner.remove_sn(t_str1) for t_str1 in user_tweets_str]
    user_tweets_clean2 = [tweet_cleaner.remove_urls(t_str2) for t_str2 in user_tweets_clean1]
    user_tweets_clean3 = [tweet_cleaner.leave_alphanumeric(t_str3) for t_str3 in user_tweets_clean2]
    user_tweets_collapse = ''.join(user_tweets_clean3)
    user_tweets_tokens = nltk.word_tokenize(user_tweets_collapse)

    fdist = FreqDist(word.lower() for word in user_tweets_tokens)
    return(fdist)