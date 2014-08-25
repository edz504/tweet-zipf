#!/usr/bin/env python
import twitter
import pandas as pd 
import numpy as np
import matplotlib.pyplot as plt
import nltk
from nltk.probability import FreqDist
from nltk.probability import ConditionalFreqDist

import tweet_cleaner

#Setting up Twitter API
twitter_api = twitter.Api(
    consumer_key='qD0K86UokYrYbqhXa4I0NWQ4i',
    consumer_secret='RAttvgN9VUmnfYNwcA8SE96qpteuTm9uwsvLUGFLgsrFrn6QL9',
    access_token_key='431244726-M96XnETmwt7fZC3Dkbuy0jsUNOpFAjFZru4z4gCZ',
    access_token_secret='S4kbwMkUrZJfYmbsohaepnnbIMd1YfEZb4IaJoUQtDQ4a')

sn = 'perezhilton'
user = twitter_api.GetUser(screen_name='perezhilton')

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

# user_tweets_clean = [tweet_cleaner.leave_alphanumeric(
#     tweet_cleaner.remove_urls(
#         tweet_cleaner.remove_sn(t) for t in user_tweets_str))]


user_tweets_collapse = ''.join(user_tweets_clean3)
user_tweets_tokens = nltk.word_tokenize(user_tweets_collapse)

fdist = FreqDist(word.lower() for word in user_tweets_tokens)


# playground below
# search = twitter_api.GetSearch(term='a', 
#     lang='en', 
#     result_type='recent', 
#     count=100, 
#     max_id='',
#     geocode= (37.781157,-122.398720, '50mi'))


# for t in search:
#     print t.user.screen_name + ' (' + t.created_at + ')'
#     #Add the .encode to force encoding
#     print t.text.encode('utf-8')
#     print ''