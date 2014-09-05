import pickle
import twitter
import tweet_retriever
import ast

#Setting up Twitter API
mine = [s.strip() for s in open('twitter_api.txt', 'rb').readlines()]
twitter_api = twitter.Api(
    consumer_key=mine[0],
    consumer_secret=mine[1],
    access_token_key=mine[2],
    access_token_secret=mine[3])

##########
sn_counter = 0   # how many users parsed
true_counter = 0 # how many users actually produced tweets we uses 
total_fdist = {}
NUM_TWEET_REQ = 1
##########
### do NOT rerun that ^^ after we started
[sn_counter, true_counter, total_fdist] = pickle.load(open('fdist1.p', 'rb'))

for sn in sns[sn_counter:]:
    try:
        ut = getUserTweets(sn)
    except Exception, e:
        d = ast.literal_eval(str(e))[0]
        error_code = d['code']
        if (error_code == 88):
            print d['message']
            break
        else:
            print 'Error: ' + d['message']
            continue
    if (len(ut) >= NUM_TWEET_REQ):
        fd = getUserTweetWordFreqDist(sn, user_tweets=ut)
        true_counter += 1
        total_fdist.update(fd)
        print sn + " freqs added"
    else:
        print sn + " did not meet NUM_TWEET_REQ"
    sn_counter += 1
    print "****Processed user " + str(sn_counter) + "****"
pickle.dump([sn_counter, true_counter, total_fdist],
    open('fdist1.p', 'wb'))

rl_stat = twitter_api.GetRateLimitStatus()
user_lookup_stat = rl_stat['resources']['statuses']['/statuses/user_timeline']
remaining = user_lookup_stat['remaining']
epoch_time = user_lookup_stat['reset']
dt_reset = datetime.datetime.fromtimestamp(epoch_time
    ).strftime('%Y-%m-%d %H:%M:%S')
print str(remaining) + ' tweets left.  Try again at ' + str(dt_reset)

plotUserTopNWords(sn=(str(true_counter) + ' random users'), n=NUM_PLOT,
    fdist=total_fdist)
#### It's not all in English :( ####

# language likelihoods?
# all swedish hmmmm but stopwords are not as useful for singular words
def get_language_likelihood(input_text):
    """Return a dictionary of languages and their likelihood of being the 
    natural language of the input text
    """
 
    input_text = input_text.lower()
    input_words = nltk.wordpunct_tokenize(input_text)
 
    language_likelihood = {}
    total_matches = 0
    for language in stopwords._fileids:
        language_likelihood[language] = len(set(input_words) &
                set(stopwords.words(language)))
 
    return language_likelihood

def get_language(input_text):
    """Return the most likely language of the given text
    """
 
    likelihoods = get_language_likelihood(input_text)
    return sorted(likelihoods, key=likelihoods.get, reverse=True)[0]

# we could use user.lang, but probably useless because (from API):

# The BCP 47 code for the user's self-declared user interface language. 
# May or may not have anything to do with the content of their Tweets.
# Examples:
# "lang": "en"
# "lang": "msa"
# "lang": "zh-cn"
