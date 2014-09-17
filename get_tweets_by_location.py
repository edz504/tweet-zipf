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
for r in rows:
    cell = r.findAll(is_cell)[6]
    str_sq_mi = cell.span.string.next
    sq_mi = float(re.sub(r'(?!\.)\W', '',  str_sq_mi.encode('utf-8'))[0:-4])
    sq_mi_list.append(sq_mi)
df['sq_mi'] = sq_mi_list

# parse out population density
dens_list = []
for r in rows:
    cell = r.findAll(is_cell)[7]
    str_pop_dens = cell.span.string.next
    pop_dens = float(re.sub(r'(?!\.)\W', '',  str_pop_dens.encode('utf-8'))[0:-7])
    dens_list.append(pop_dens)
df['pop_dens'] = dens_list

# lat and lon
lat_list = []
lng_list = []
for r in rows:
    cell = r.findAll(is_cell)[8]
    str_latlng = re.sub(r'(?!\.)(?!\s)\W', '', cell.string.encode('utf-8'))
    lat_list.append(float(str_latlng.split(' ')[0][0:-1])) #spot the N
    lng_list.append(float(str_latlng.split(' ')[1][0:-1])) # and the W
df['lat'] = lat_list
df['lng'] = lng_list

# adding Princeton and Palo Alto by hand <3
df.loc['Princeton, New Jersey'] = [17.933, 1600, 40.357830, -74.667396]
df.loc['Palo Alto, California'] = [23.884, 2500, 37.442494, -122.142961]

import numpy as np
# calculating radius from square miles (obviously approximation)
df['rad'] = np.sqrt(df['sq_mi'] / 2)

df['geocode_query'] = [str(df['lat'][i]) + "," + str(df['lng'][i]) + \
"," + str(df['rad'][i]) + "mi" for i in range(0, df.shape[0])]


results = api.search(q="", geocode=df['geocode_query'][0], count=100,
    result_type = "recent")