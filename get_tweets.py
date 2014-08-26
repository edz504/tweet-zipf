#!/usr/bin/env python
import twitter
import pandas as pd 
import numpy as np
import matplotlib.pyplot as plt
import pylab as pl
import nltk
import operator
from nltk.probability import FreqDist
from nltk.probability import ConditionalFreqDist

import tweet_cleaner

#Setting up Twitter API
twitter_api = twitter.Api(
    consumer_key='qD0K86UokYrYbqhXa4I0NWQ4i',
    consumer_secret='RAttvgN9VUmnfYNwcA8SE96qpteuTm9uwsvLUGFLgsrFrn6QL9',
    access_token_key='431244726-M96XnETmwt7fZC3Dkbuy0jsUNOpFAjFZru4z4gCZ',
    access_token_secret='S4kbwMkUrZJfYmbsohaepnnbIMd1YfEZb4IaJoUQtDQ4a')

def getUserTweetWordFreqDist(sn):
    user = twitter_api.GetUser(screen_name=sn)

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
        if len(this_user_tweets) == 1:
            keep_em_coming = False
        oldest_id = min([t.id for t in this_user_tweets])
        user_tweets += this_user_tweets
        
    user_tweets_str = [t.text.encode('utf-8') for t in user_tweets]

    user_tweets_clean1 = [tweet_cleaner.remove_sn(t_str1) for t_str1 in user_tweets_str]

    user_tweets_clean2 = [tweet_cleaner.remove_urls(t_str2) for t_str2 in user_tweets_clean1]

    user_tweets_clean3 = [tweet_cleaner.leave_alphanumeric(t_str3) for t_str3 in user_tweets_clean2]

    user_tweets_collapse = ''.join(user_tweets_clean3)
    user_tweets_tokens = nltk.word_tokenize(user_tweets_collapse)

    fdist = FreqDist(word.lower() for word in user_tweets_tokens)
    return(fdist)

def plotUserTopNWords(sn, n, fdist=None):
    if fdist is None:
        print 'Getting tweets for ' + sn
        fdist = getUserTweetWordFreqDist(sn)
    fsort_tuple = sorted(fdist.items(), key=operator.itemgetter(1),
        reverse=True)
    freqs_np_vals = np.array([t[1] for t in fsort_tuple])[0:n]
    freqs_np_words = np.array([t[0] for t in fsort_tuple])[0:n]
    width = .35
    ind = np.arange(len(freqs_np_vals))
    plt.title('Ranked Word Counts in the Tweets of ' + sn)
    plt.bar(ind, freqs_np_vals)
    plt.xticks(ind + width / 2, freqs_np_words, rotation='vertical')
    mng = plt.get_current_fig_manager()
    mng.window.state('zoomed')
    plt.show()


sn = 'edz504'
NUM_PLOT = 80
plotUserTopNWords(sn=sn, n=NUM_PLOT, fdist = fdist)

# Want to aggregate a bunch of tweets, random users 
import sys
from random import randint

users = []
while (len(users) < 100):
    uid = randint(1, sys.maxint)
    try:
        user = twitter_api.GetUser(user_id=uid)
    except:
        continue
    users.append(user)
    print(len(users))