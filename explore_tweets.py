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
import tweet_cleaner
import tweet_retriever

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


sn = 'perezhilton'
NUM_PLOT = 80
plotUserTopNWords(sn=sn, n=NUM_PLOT)

users = pickle.load(open('users1.p', 'rb'))
sns = [u.screen_name for u in users]

NUM_TWEET_CUTOFF = 10
lang_users = [u for u in users if u.statuses_count > NUM_TWEET_CUTOFF]
