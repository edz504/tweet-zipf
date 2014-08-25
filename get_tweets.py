#!/usr/bin/env python
import twitter
import pandas as pd 
import numpy as np
import matplotlib.pyplot as plt

#Setting up Twitter API
twitter_api = twitter.Api(
    consumer_key='qD0K86UokYrYbqhXa4I0NWQ4i',
    consumer_secret='RAttvgN9VUmnfYNwcA8SE96qpteuTm9uwsvLUGFLgsrFrn6QL9',
    access_token_key='431244726-M96XnETmwt7fZC3Dkbuy0jsUNOpFAjFZru4z4gCZ',
    access_token_secret='S4kbwMkUrZJfYmbsohaepnnbIMd1YfEZb4IaJoUQtDQ4a')

# we want to aggregate a large number of tweets and investigate the following:
# - does a corpus assembled from tweets from a certain area follow Zipf's Law?
# - does a corpus assembled from one user's tweets follow Zipf's Law?


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