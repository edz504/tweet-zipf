import tweepy

mine = [s.strip() for s in open('twitter_api.txt', 'rb').readlines()]
# OAuth process, using the keys and tokens
auth = tweepy.OAuthHandler(mine[0], mine[1])
auth.set_access_token(mine[2], mine[3])
 
# Creation of the actual interface, using authentication
api = tweepy.API(auth)
PTON = "40.346971,-74.660449"
RAD = "10mi"

results = api.search(q="", geocode=PTON + "," + RAD, count=100)