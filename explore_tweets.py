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
from nltk.corpus import brown, reuters, nps_chat, webtext

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
    plt.title(sn)
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

#### Does an individual user follow Zipf's Law?           ####
#### If not, do they all follow a different distribution? ####

# first, explore Zipf's Law on known corpora
brown_fdist = nltk.FreqDist(w.lower() for w in brown.words())
# only leave numbers (does the rest count as "language"? tricky)
word_only_keys = [k for k in brown_fdist.keys() if re.search(r'^[a-zA-Z]+$',
    k)]
brown_fdist_letters = { key : brown_fdist[key] for key in word_only_keys }
plotUserTopNWords(sn='Brown Corpus', n=NUM_PLOT, fdist=brown_fdist_letters)

reut_fdist = nltk.FreqDist(w.lower() for w in reuters.words())
word_only_keys = [k for k in reut_fdist.keys() if re.search(r'^[a-zA-Z]+$',
    k)]
reut_fdist_letters = { key : reut_fdist[key] for key in word_only_keys }
plotUserTopNWords(sn='Reuters Corpus', n=NUM_PLOT, fdist=reut_fdist_letters)

nps_fdist = nltk.FreqDist(w.lower() for w in nps_chat.words())
word_only_keys = [k for k in nps_fdist.keys() if re.search(r'^[a-zA-Z]+$',
    k)]
nps_fdist_letters = { key : nps_fdist[key] for key in word_only_keys }
plotUserTopNWords(sn='nps_chat Corpus', n=NUM_PLOT, fdist=nps_fdist_letters)

# just so we don't have to recalculate those fdists
pickle.dump([brown_fdist_letters, reut_fdist_letters, nps_fdist_letters],
    open('known_fdist.p', 'wb'))

# looks like brown and reuters follow Zipf's quite well, whereas nps_chat 
# not so much.


# we only want users that have tweeted at least X times
NUM_TWEET_CUTOFF = 10
lang_users = [u for u in users if u.statuses_count > NUM_TWEET_CUTOFF]

