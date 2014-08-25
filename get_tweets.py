#!/usr/bin/env python
import twitter
import pandas as pd 
import numpy as np
import matplotlib.pyplot as plt
import re
import nltk
from nltk.probability import FreqDist
from nltk.probability import ConditionalFreqDist

#Setting up Twitter API
twitter_api = twitter.Api(
    consumer_key='qD0K86UokYrYbqhXa4I0NWQ4i',
    consumer_secret='RAttvgN9VUmnfYNwcA8SE96qpteuTm9uwsvLUGFLgsrFrn6QL9',
    access_token_key='431244726-M96XnETmwt7fZC3Dkbuy0jsUNOpFAjFZru4z4gCZ',
    access_token_secret='S4kbwMkUrZJfYmbsohaepnnbIMd1YfEZb4IaJoUQtDQ4a')
    
sn = 'perezhilton'
user = twitter_api.GetUser(screen_name='perezhilton')
user_tweets = twitter_api.GetUserTimeline(screen_name=sn,
    count=200)

user_tweets_str = [t.text.encode('utf-8') for t in user_tweets]
# we included replies, and we want to keep them, but we don't want to include
# other people's screen_names in the string

# basic function to remove screen name
# has not been scrutinized, will probably fail on some stuff
def remove_sn(t):
    rep = 0
    ats_cleaned = True
    if ('@' in t):
        ats_cleaned = False
    while(not ats_cleaned):
        at_ind_start = t.index('@')
        # the space should really be any non-screen-name-enabled character
        # so if the tweet is "...@Beyonce:blahhh "
        # then we leave blahhh in the string too
        m = re.search(r'\W', t[at_ind_start + 1:])
        if m:
            at_ind_end = at_ind_start + m.start()
        else:
            at_ind_end = at_ind_start + len(t[at_ind_start:])
        t = t[:at_ind_start] + t[at_ind_end + 1:]
        if (not '@' in t):
            ats_cleaned = True
        if (rep > 140):
            print 'Reached' + str(rep) + ' repetitions for the string:'
            print t
            print 'at index ' + rep + 'breaking'
            break
        rep += 1
    return(t)

user_tweets_clean1 = [remove_sn(t_str1) for t_str1 in user_tweets_str]

# now let's remove urls (they're definitely not words)
def remove_urls(t):
    urls = re.findall(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+',
        t)
    for url in urls:
        t = re.sub(url, '', t)
    return(t)

user_tweets_clean2 = [remove_urls(t_str2) for t_str2 in user_tweets_clean1]

# now that we have taken care of the screen_names with the @'s, as well as
# the URLs, we can remove all punctuation.  note that this leaves hashtags
# (words that follow the # sign) in the string, because we believe this 
# should count as a word (or words)
def leave_alphanumeric(t):
    return re.sub(r'(?! )(?!-)(?!\')\W', '', t)
user_tweets_clean3 = [leave_alphanumeric(t_str3) for t_str3 in user_tweets_clean2]

user_tweets_collapse = ''.join(user_tweets_clean3)
user_tweets_tokens = nltk.word_tokenize(user_tweets_collapse)

fdist = FreqDist(word.lower() for word in user_tweets_tokens)


# playground below
search = twitter_api.GetSearch(term='a', 
    lang='en', 
    result_type='recent', 
    count=100, 
    max_id='',
    geocode= (37.781157,-122.398720, '50mi'))


for t in search:
    print t.user.screen_name + ' (' + t.created_at + ')'
    #Add the .encode to force encoding
    print t.text.encode('utf-8')
    print ''