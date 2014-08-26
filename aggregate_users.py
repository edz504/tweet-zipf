#!/usr/bin/env python
import twitter
import pickle

#Setting up Twitter API
twitter_api = twitter.Api(
    consumer_key='qD0K86UokYrYbqhXa4I0NWQ4i',
    consumer_secret='RAttvgN9VUmnfYNwcA8SE96qpteuTm9uwsvLUGFLgsrFrn6QL9',
    access_token_key='431244726-M96XnETmwt7fZC3Dkbuy0jsUNOpFAjFZru4z4gCZ',
    access_token_secret='S4kbwMkUrZJfYmbsohaepnnbIMd1YfEZb4IaJoUQtDQ4a')

# Want to aggregate random users 
import sys, json
import datetime
from random import randint

users = []
while (len(users) < 100):
    uid = randint(1, sys.maxint)
    try:
        these_users = twitter_api.GetUser(user_id=uid)
    except Exception, e:
        d = ast.literal_eval(str(e))[0]
        error_code = d['code']
        if (error_code == 88):
            print d['message']
            rl_stat = twitter_api.GetRateLimitStatus()
            user_lookup_stat = rl_stat['resources']['users']['/users/show/:id']
            remaining = user_lookup_stat['remaining']
            epoch_time = user_lookup_stat['reset']
            dt_reset = datetime.datetime.fromtimestamp(epoch_time
                ).strftime('%Y-%m-%d %H:%M:%S')
            print str(remaining) + ' tweets left.  Try again at ' + str(dt_reset)
            break
        else:
            print 'Error: ' + d['message']
            continue
    users.append(user)
    print(len(users))

# using pickle to save the users in a python data file
pickle.dump(users, open('users1.p', 'wb'))



# using users_lookup which allows for lookup of 100 users in one request.
# goddammmit.

while (len(users) < 10000):
    uids = [randint(1, sys.maxint) for i in range(1, 100)]
    try:
        these_users = twitter_api.UsersLookup(user_id=uids)
    except Exception, e:
        d = ast.literal_eval(str(e))[0]
        error_code = d['code']
        if (error_code == 88):
            print d['message']
            rl_stat = twitter_api.GetRateLimitStatus()
            user_lookup_stat = rl_stat['resources']['users']['/users/show/:id']
            remaining = user_lookup_stat['remaining']
            epoch_time = user_lookup_stat['reset']
            dt_reset = datetime.datetime.fromtimestamp(epoch_time
                ).strftime('%Y-%m-%d %H:%M:%S')
            print str(remaining) + ' tweets left.  Try again at ' + str(dt_reset)
            break
        else:
            print 'Error: ' + d['message']
            continue
    users += these_users
    print(len(users))
pickle.dump(users, open('users1.p', 'wb'))
