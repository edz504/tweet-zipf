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
from nltk.corpus import brown, reuters, nps_chat
    
from dateutil import parser
import time
import ggplot

def plotFdist(n, title=None, fdist=None):
    fsort_tuple = sorted(fdist.items(), key=operator.itemgetter(1),
        reverse=True)
    freqs_np_vals = np.array([t[1] for t in fsort_tuple])[0:n]
    freqs_np_words = np.array([t[0] for t in fsort_tuple])[0:n]
    width = .35
    ind = np.arange(len(freqs_np_vals))
    plt.title(title)
    plt.bar(ind, freqs_np_vals)
    plt.xticks(ind + width / 2, freqs_np_words, rotation='vertical')
    mng = plt.get_current_fig_manager()
    mng.window.state('zoomed')
    plt.show()

# first, explore Zipf's Law on known corpora
def wordOnlyFDist(fdist):
    # only leave letters (does the rest count as "language"? tricky)
    word_only_keys = [k for k in fdist.keys() if re.search(r'^[a-zA-Z]+$',
        k)]
    return({ key : fdist[key] for key in word_only_keys })

### commmented out because we can load from pickle ###
[brown_fdist, reut_fdist, nps_fdist] = pickle.load(
    open('known_fdist.p', 'rb'))

NUM_PLOT = 50
# brown_fdist = nltk.FreqDist(w.lower() for w in brown.words())
plotFdist(n=NUM_PLOT, title='Brown Corpus',
    fdist=wordOnlyFDist(brown_fdist))

# reut_fdist = nltk.FreqDist(w.lower() for w in reuters.words())
plotFdist(n=NUM_PLOT, title='Reuters Corpus', 
    fdist=wordOnlyFDist(reut_fdist))

# nps_fdist = nltk.FreqDist(w.lower() for w in nps_chat.words())
plotFdist(n=NUM_PLOT, title='nps_chat Corpus', 
    fdist=wordOnlyFDist(nps_fdist))

# just so we don't have to recalculate those fdists
pickle.dump([brown_fdist, reut_fdist, nps_fdist],
    open('known_fdist.p', 'wb'))

from scipy import stats

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

import tweet_cleaner
import tweet_retriever

#Setting up Twitter API
mine = [s.strip() for s in open('twitter_api.txt', 'rb').readlines()]
twitter_api = twitter.Api(
    consumer_key=mine[0],
    consumer_secret=mine[1],
    access_token_key=mine[2],
    access_token_secret=mine[3])



def plotUserTopNWords(n, u=None, title=None, fdist=None):
    if title is None and (u is not None):
        title = u.screen_name
    if fdist is None and (u is not None):
        print 'Getting tweets for ' + u.screen_name
        fdist = tweet_retriever.getUserTweetWordFreqDist(u)
    fsort_tuple = sorted(fdist.items(), key=operator.itemgetter(1),
        reverse=True)
    freqs_np_vals = np.array([t[1] for t in fsort_tuple])[0:n]
    freqs_np_words = np.array([t[0] for t in fsort_tuple])[0:n]
    width = .35
    ind = np.arange(len(freqs_np_vals))
    plt.title(title)
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

fdist = tweet_retriever.getUserTweetWordFreqDist(
    twitter_api.GetUser(screen_name='perezhilton'))
zipfFit(wordOnlyFDist(fdist), 'perezhilton', pl=True, pr=True, ret=False)



# we only want users that have tweeted at least X times
NUM_TWEET_CUTOFF = 1
lang_users = [u for u in users if u.statuses_count > NUM_TWEET_CUTOFF]
# also, filter out protected peeps
end_users = [u for u in lang_users if (not u.protected)]
col = [
    'num_fit', 'r_squared', 'slope', 'intercept', 'statuses_count', 
    'followers_count', 'following_count', 'age_days',
    'favourites_count', 'location', 'verified'
]
df = pd.DataFrame(index=[u.screen_name for u in end_users],
    columns=col)
df['statuses_count'] = [u.statuses_count for u in end_users]
df['followers_count'] = [u.followers_count for u in end_users]
df['following_count'] = [u.friends_count for u in end_users]
df['favourites_count'] = [u.favourites_count for u in end_users]
df['location'] = [u.location for u in end_users]
df['verified'] = [u.verified for u in end_users]
# make a list comprehension to calculate age in days from Twitter's founding
# http://www.usatoday.com/story/tech/2014/03/20/twitter-eighth-birthday-first-tweet/6646493/
# ^ says that March 21st, 2006 is the oldest Tweet
import pytz
epoch = parser.parse("Mar 21 2006 13:33:00").replace(tzinfo=pytz.UTC)
df['age_days'] = [(parser.parse(u.created_at) - epoch).days for u in end_users]

i = 0
STOPPED = 0

for u in end_users[STOPPED:]:
    # get as many tweets as possible for that user, assembling the tweets 
    # into a corpus, clean and create an fdist
    try:
        # the getUserTweetWordFreqDist can retrieve the tweets on its own,
        # but we also want to see how many tweets we use for the fit
        tweets = tweet_retriever.getUserTweets(u)
        fdist = tweet_retriever.getUserTweetWordFreqDist(u, tweets)
    except Exception, e:
        d = ast.literal_eval(str(e))[0]
        error_code = d['code']
        if (error_code == 88):
            print d['message']
        print 'Currently, u = ' + u.screen_name + ', i = ' + str(i)
        STOPPED = i
        # break
        # save to pickle
        pickle.dump([STOPPED, df], open('zipf_fit_df.p', 'wb')) 
        print 'Pausing for 15 minutes...'
        time.sleep(5 * 60)
        print '.'
        time.sleep(5 * 60)
        print '.'
        time.sleep(5 * 60)
        print 'Re-finding tweets'
        tweets = tweet_retriever.getUserTweets(u)
        fdist = tweet_retriever.getUserTweetWordFreqDist(u, tweets)
    fdist_wordsOnly = wordOnlyFDist(fdist)
    # fit the fdist to Zipf's
    slope, intercept, r_squared = zipfFit(fdist_wordsOnly, 
        u.screen_name)
    # record stats
    df['num_fit'][i] = len(set(tweets))
    df['r_squared'][i] = r_squared
    df['slope'][i] = slope
    df['intercept'][i] = intercept
    i += 1
    print 'Finished <' + u.screen_name + '>'


rl_stat = twitter_api.GetRateLimitStatus()
user_lookup_stat = rl_stat['resources']['statuses']['/statuses/user_timeline']
remaining = user_lookup_stat['remaining']
epoch_time = user_lookup_stat['reset']
dt_reset = datetime.datetime.fromtimestamp(epoch_time
    ).strftime('%Y-%m-%d %H:%M:%S')
print str(remaining) + ' requests left.  Try again at ' + str(dt_reset)

# if we want to do more specific analysis w.r.t these variables and the
# actual fdists (not just their Zipf-fit, we will have these stored in a df)


# definitely graphing with R
# http://www.r-bloggers.com/ggplot2-in-python-a-major-barrier-broken/
# or 
# http://blog.yhathq.com/posts/ggplot-for-python.html