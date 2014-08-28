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
import pickle
import ast
import datetime
import re
from nltk.corpus import brown, reuters, nps_chat, webtext
from scipy import stats

import tweet_cleaner
import tweet_retriever

#Setting up Twitter API
twitter_api = twitter.Api(
    consumer_key='qD0K86UokYrYbqhXa4I0NWQ4i',
    consumer_secret='RAttvgN9VUmnfYNwcA8SE96qpteuTm9uwsvLUGFLgsrFrn6QL9',
    access_token_key='431244726-M96XnETmwt7fZC3Dkbuy0jsUNOpFAjFZru4z4gCZ',
    access_token_secret='S4kbwMkUrZJfYmbsohaepnnbIMd1YfEZb4IaJoUQtDQ4a')

def plotUserTopNWords(u, n, fdist=None):
    if fdist is None:
        print 'Getting tweets for ' + u.screen_name
        fdist = tweet_retriever.getUserTweetWordFreqDist(u)
    fsort_tuple = sorted(fdist.items(), key=operator.itemgetter(1),
        reverse=True)
    freqs_np_vals = np.array([t[1] for t in fsort_tuple])[0:n]
    freqs_np_words = np.array([t[0] for t in fsort_tuple])[0:n]
    width = .35
    ind = np.arange(len(freqs_np_vals))
    plt.title(u.screen_name)
    plt.bar(ind, freqs_np_vals)
    plt.xticks(ind + width / 2, freqs_np_words, rotation='vertical')
    mng = plt.get_current_fig_manager()
    mng.window.state('zoomed')
    plt.show()


sn = 'perezhilton'
NUM_PLOT = 80
plotUserTopNWords(u=twitter_api.GetUser(screen_name=sn),
    n=NUM_PLOT)

users = pickle.load(open('users1.p', 'rb'))

# first, explore Zipf's Law on known corpora
def wordOnlyFDist(fdist):
    # only leave numbers (does the rest count as "language"? tricky)
    word_only_keys = [k for k in fdist.keys() if re.search(r'^[a-zA-Z]+$',
        k)]
    return({ key : fdist[key] for key in word_only_keys })

### commmented out because we can load from pickle ###
[brown_fdist, reut_fdist, nps_fdist] = pickle.load(
    open('known_fdist.p', 'rb'))

# brown_fdist = nltk.FreqDist(w.lower() for w in brown.words())
plotUserTopNWords(sn='Brown Corpus', n=NUM_PLOT, 
    fdist=wordOnlyFDist(brown_fdist))

# reut_fdist = nltk.FreqDist(w.lower() for w in reuters.words())
plotUserTopNWords(sn='Reuters Corpus', n=NUM_PLOT, 
    fdist=wordOnlyFDist(reut_fdist))

# nps_fdist = nltk.FreqDist(w.lower() for w in nps_chat.words())
plotUserTopNWords(sn='nps_chat Corpus', n=NUM_PLOT, 
    fdist=wordOnlyFDist(nps_fdist))

# just so we don't have to recalculate those fdists
# pickle.dump([brown_fdist, reut_fdist, nps_fdist],
#     open('known_fdist.p', 'wb'))

def zipfFit(fdist, name, pl=False, pr=False, ret=True):
    fsort_tuple = sorted(fdist.items(), key=operator.itemgetter(1),
    reverse=True)
    y_vals = np.array([t[1] for t in fsort_tuple])
    x_vals = np.array(range(1, len(y_vals) + 1))
    if pl:
        plt.plot([np.log(x) for x in x_vals], 
            [np.log(y) for y in y_vals], 'ro')
        plt.show()
    slope, intercept, r_value, p_value, std_err = stats.linregress(
        np.log(x_vals.astype(float)),
        np.log(y_vals.astype(float)))
    if pr:
        print "log-log r-squared for " + name + ":", r_value**2
    if ret:
        return([slope, intercept, r_value**2])

# looks like brown and reuters follow Zipf's quite well, whereas nps_chat 
# not so much.  we can quantify this with an actual fit
zipfFit(wordOnlyFDist(brown_fdist), 'brown', pl=True, pr=True, ret=False)
zipfFit(wordOnlyFDist(reut_fdist), 'reuters', pl=True, pr=True, ret=False)
zipfFit(wordOnlyFDist(nps_fdist), 'nps_chat', pl=True, pr=True, ret=False)


#### Do the tweets of an individual user follow Zipf's Law?                 ####
#### If not, do they all follow a different distribution?                   ####
#### If so, what kind of users are likely to follow Zipf's Law?             ####
#### Does a compilation of random tweets follow Zipf's Law?                 ####
#### Does a set of random tweets geographically linked follow Zipf's Law?   ####

fdist = tweet_retriever.getUserTweetWordFreqDist(
    twitter_api.GetUser(screen_name='perezhilton'))
zipfFit(wordOnlyFDist(fdist), 'perezhilton', pl=True, pr=True, ret=False)

# we only want users that have tweeted at least X times
NUM_TWEET_CUTOFF = 1
lang_users = [u for u in users if u.statuses_count > NUM_TWEET_CUTOFF]

col = [
    'num_fit', 'r_squared', 'slope', 'intercept', 'statuses_count', 
    'followers_count', 'following_count', 'age',
    'favourites_count', 'location', 'verified'
]
df = pd.DataFrame(index=[u.screen_name for u in lang_users],
    columns=col)
df['statuses_count'] = [u.statuses_count for u in lang_users]
df['followers_count'] = [u.followers_count for u in lang_users]
df['following_count'] = [u.friends_count for u in lang_users]
# make a list comprehension to calculate age in days from Twitter's founding
# http://www.usatoday.com/story/tech/2014/03/20/twitter-eighth-birthday-first-tweet/6646493/
# ^ says that March 21st, 2006 is the oldest Tweet
# df['age'] = [u.followers_count for u in lang_users]
df['favourites_count'] = [u.favourites_count for u in lang_users]
df['location'] = [u.location for u in lang_users]
df['verified'] = [u.verified for u in lang_users]

for u in lang_users:
    # get as many tweets as possible for that user, assembling the tweets 
    # into a corpus, clean and create an fdist
    fdist = tweet_retriever.getUserTweetWordFreqDist(u)
    fdist_wordsOnly = wordOnlyFDist(fdist)
    # fit the fdist to Zipf's
    slope, intercept, r_squared = zipfFit(fdist_wordsOnly, 
        u.screen_name)
    # record stats

# if we want to do more specific analysis w.r.t these variables and the
# actual fdists (not just their Zipf-fit, we will have these stored in a df)
