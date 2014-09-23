import pickle
import pandas as pd
import numpy as np

df = pickle.load(open('location_df.p', 'rb'))
[STOPPED, city_fdist] = pickle.load(open('city_tweets.p', 'rb'))

def getLexDiv(fdist):
    if sum(fdist.values()) == 0:
        return np.nan
    return len(fdist.keys()) / float(sum(fdist.values()))
# compute lexicographical diversity
lex_div = [getLexDiv(city) for city in city_fdist]

df['lex_div'] = lex_div