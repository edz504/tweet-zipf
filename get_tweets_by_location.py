import tweepy

mine = [s.strip() for s in open('twitter_api.txt', 'rb').readlines()]
# OAuth process, using the keys and tokens
auth = tweepy.OAuthHandler(mine[0], mine[1])
auth.set_access_token(mine[2], mine[3])
 
# Creation of the actual interface, using authentication
api = tweepy.API(auth)

import requests
from bs4 import BeautifulSoup

url = 'http://en.wikipedia.org/wiki/List_of_United_States_cities_by_population'
r = requests.get(url)
soup = BeautifulSoup(r.text)

def is_table_row(tag):
    return tag.name == 'tr' and (tag.td is not None) and \
    (tag.td.string in [str(i) for i in range(1, 251)])

rows = soup.findAll(is_table_row)
ranks = [tr.td.string for tr in rows]

rows = rows[:-5] # to get rid of Puerto Rican cities

def is_cell(tag):
    return tag.name == 'td'

cells = rows[0].findAll(is_cell)

import re
def clean_name(s):
    return re.sub(r'(?!\s)\W|[0-9]', '', s)

import pandas as pd
col = ['sq_mi', 'pop_dens', 'lat', 'lng']
df = pd.DataFrame(index=[clean_name(r.findAll(is_cell)[1].text) + ", " + \
    clean_name(r.findAll(is_cell)[2].text) for r in rows],
    columns=col)

# parse out square miles
sq_mi_list = []
dens_list = []
lat_list = []
lng_list = []
# I CLEANED OUT ALL THE NEGATIVE SIGNS
for r in rows:
    cell = r.findAll(is_cell)[6]
    str_sq_mi = cell.span.string.next
    sq_mi = float(re.sub(r'(?!\.)\W', '',  str_sq_mi.encode('utf-8'))[0:-4])
    sq_mi_list.append(sq_mi)

    cell = r.findAll(is_cell)[7]
    str_pop_dens = cell.span.string.next
    pop_dens = float(re.sub(r'(?!\.)\W', '',  str_pop_dens.encode('utf-8'))[0:-7])
    dens_list.append(pop_dens)

    cell = r.findAll(is_cell)[8]
    str_latlng = re.sub(r'(?!\.)(?!\s)\W', '', cell.string.encode('utf-8'))
    lat_list.append(float(str_latlng.split(' ')[0][0:-1])) #spot the N
    lng_list.append(-float(str_latlng.split(' ')[1][0:-1])) # and the W
df['sq_mi'] = sq_mi_list
df['pop_dens'] = dens_list
df['lat'] = lat_list
df['lng'] = lng_list

# adding Princeton and Palo Alto by hand <3
df.loc['Princeton, New Jersey'] = [17.933, 1600, 40.357830, -74.667396]
df.loc['Palo Alto, California'] = [23.884, 2500, 37.442494, -122.142961]

import numpy as np
# calculating radius from square miles (obviously approximation)
df['rad'] = np.sqrt(df['sq_mi'] / 2)

# (26.9 miles) / hour * (25.4 min) * (1 hour / 60 min) ==> 11.387
# add for the suburbs (anything within average commute distance)
# http://project.wnyc.org/commute-times-us/embed.html#5.00/42.000/-89.500
# http://nhts.ornl.gov/briefs/Commuting%20for%20Life.pdf
df['rad'] = df['rad'] + 26.9 * 25.4 / 60

df['geocode_query'] = [str(df['lat'][i]) + "," + str(df['lng'][i]) + \
"," + str(df['rad'][i]) + "mi" for i in range(0, df.shape[0])]

import pickle
pickle.dump(df, open('location_df.p', 'wb'))
# same method as before, didn't want to import
def wordOnlyFDist(fdist):
    # only leave letters (does the rest count as "language"? tricky)
    word_only_keys = [k for k in fdist.keys() if re.search(r'^[a-zA-Z]+$',
        k)]
    return({ key : fdist[key] for key in word_only_keys })

## let's move the sleep to here
def get_geo_tweets(gq):
    keep_em_coming = True
    total_results = []
    while (keep_em_coming):
        if len(total_results) == 0: # for first time
            results = api.search(q="", geocode=gq, count=200)
        else:
            try:
                results = api.search(q="", geocode=gq, count=200,
                    max_id = oldest_id - 1)
            except Exception, e:
                d = ast.literal_eval(str(e))[0]
                error_code = d['code']
                if (error_code == 88):
                    print d['message']
                print 'Current city: ' + df.index[i] + ', i = ' + str(i)
                STOPPED = i
                print 'Pausing for 15 minutes...'
                time.sleep(5 * 60)
                print '.'
                time.sleep(5 * 60)
                print '.'
                time.sleep(5 * 60)
                print 'Re-finding tweets'
                results = api.search(q="", geocode=gq, count=200,
                    max_id = oldest_id - 1)
        print "Pulled in " + str(len(results)) + " tweets"
        if len(results) <= 1:
            keep_em_coming = False
        else:
            oldest_id = min([t.id for t in results])
        total_results += results
        if (len(total_results) > 10000): # put in limit
            return(total_results)
    return(total_results)

import ast, time
import tweet_retriever

####
city_fdist = []
STOPPED = 0
city_tweets = []
# or # 
[STOPPED, city_fdist] = pickle.load(open('city_fdist.p', 'rb'))
city_tweets = pickle.load(open('city_tweets.p', 'rb'))
####
for i in range(STOPPED, df.shape[0]):
    gq = df['geocode_query'][i]
    total_results = get_geo_tweets(gq)
    tweet_text = [t.text for t in total_results]
    city_tweets.append(tweet_text)
    pickle.dump(city_tweets, open('city_tweets.p', 'wb'))
    print "Finished collecting " + df.index[i]
    fdist = tweet_retriever.getUserTweetWordFreqDist(
        user_tweets=total_results)
    fdist_wordsOnly = wordOnlyFDist(fdist)
    city_fdist.append(fdist_wordsOnly)
    pickle.dump([STOPPED, city_fdist], open('city_fdist.p', 'wb'))

# note: we should probably store the tweets at each request, not just at each city
# because we could hit the limit within one city



####
# something we notice is that some of these big cities don't have
# many Twitter users
# that may depend on time of day, because we have "recent"

# take out the ones that don't have at least 100

# we can use ggmaps to plot zipfian fits by city!!