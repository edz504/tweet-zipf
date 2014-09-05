#!/usr/bin/env python
import twitter
import pickle
import ast

#Setting up Twitter API
mine = [s.strip() for s in open('twitter_api.txt', 'rb').readlines()]
twitter_api = twitter.Api(
    consumer_key=mine[0],
    consumer_secret=mine[1],
    access_token_key=mine[2],
    access_token_secret=mine[3])

# Want to aggregate random users 
import sys, json
import datetime
from random import randint

users = []
# while (len(users) < 100):
#     uid = randint(1, sys.maxint)
#     try:
#         these_users = twitter_api.GetUser(user_id=uid)
#     except Exception, e:
#         d = ast.literal_eval(str(e))[0]
#         error_code = d['code']
#         if (error_code == 88):
#             print d['message']
#             rl_stat = twitter_api.GetRateLimitStatus()
#             user_lookup_stat = rl_stat['resources']['users']['/users/show/:id']
#             remaining = user_lookup_stat['remaining']
#             epoch_time = user_lookup_stat['reset']
#             dt_reset = datetime.datetime.fromtimestamp(epoch_time
#                 ).strftime('%Y-%m-%d %H:%M:%S')
#             print str(remaining) + ' tweets left.  Try again at ' + str(dt_reset)
#             break
#         else:
#             print 'Error: ' + d['message']
#             continue
#     users.append(user)
#     print(len(users))

# # using pickle to save the users in a python data file
# pickle.dump(users, open('users1.p', 'wb'))



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
            user_lookup_stat = rl_stat['resources']['users']['/users/lookup']
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
