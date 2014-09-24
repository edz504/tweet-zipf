import pickle
import pandas as pd
import numpy as np

df = pickle.load(open('location_df.p', 'rb'))
[STOPPED, city_fdist] = pickle.load(open('city_fdist.p', 'rb'))

from scipy import stats
import operator
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

# compute lexical richness
def getLexDiv(fdist):
    if sum(fdist.values()) == 0:
        return np.nan
    return len(fdist.keys()) / float(sum(fdist.values()))

lex_div = [getLexDiv(city) for city in city_fdist]
zipf_fits = []
i = 0
for city in city_fdist:
    slope, intercept, r_squared = zipfFit(city, df.index[i])
    zipf_fits.append(r_squared)
    i += 1

# most common words in each city?
top = [max(city.iteritems(), 
    key=operator.itemgetter(1))[0] for city in city_fdist]

dump_df = df.iloc[0:101,:].drop('geocode_query', 1)
dump_df['lex_div'] = lex_div
dump_df['zipf_fit'] = zipf_fits
dump_df['top_word'] = top
f = 'cities.csv'
dump_df.to_csv(f)