import twitter
import pandas as pd 
import numpy as np
import matplotlib.pyplot as plt
import pylab as pl
import pickle

mine = [s.strip() for s in open('twitter_api.txt', 'rb').readlines()]
twitter_api = twitter.Api(
    consumer_key=mine[0],
    consumer_secret=mine[1],
    access_token_key=mine[2],
    access_token_secret=mine[3])

[STOPPED, df] = pickle.load(open('zipf_fit_df.p', 'rb'))

#### exploring what we gathered ####
print df['r_squared'].astype(float).describe()


ZCUT = 0.95
# we'll say that a user adheres to Zipf's if their log-log r_squared
# is greater than 0.95 (~ 0.96, 0.97 for the existing corpora)
df_fit = df[df.r_squared >= ZCUT]
df_nfit = df[df.r_squared < ZCUT]
print df_fit.describe()
print df_nfit.describe()

df_quant = df[['num_fit', 'r_squared', 'slope',
    'intercept', 'statuses_count', 'followers_count',
    'following_count', 'age_days', 'favourites_count']].astype(float)
df_clean = df_quant.dropna()

## visualization
df_vis = df_clean.loc[df_clean.index != df['followers_count'].argmax()]
df_vis = df_vis.loc[df_vis['favourites_count'] >= 1]
df_vis['zipf'] = (df_vis.r_squared >= 0.96).astype(int)

from ggplot import *

print ggplot(df_vis, aes(x='followers_count', y='r_squared', 
    colour='zipf')) + geom_point(aes(color='zipf'))

# print ggplot(aes(fill='zipf', x='zipf', y='r_squared'), 
#     data=df_vis) + geom_boxplot()

print ggplot(df_vis, aes(x='statuses_count', 
    fill='zipf')) + geom_density(alpha=0.3)

print ggplot(df_vis, aes(x='followers_count', 
    fill='zipf')) + geom_density(alpha=0.3)

print ggplot(df_vis, aes(x='following_count', 
    fill='zipf')) + geom_density(alpha=0.3)

print ggplot(df_vis, aes(x='age_days', 
    fill='zipf')) + geom_density(alpha=0.3)

# we want to see what characteristics of users differentiate those that
# fit Zipf's well and those that don't.  to do that, we can build classifiers
# and look at the coefficients to see which features are important

X = df_clean.drop(['r_squared', 'slope', 'intercept'], axis=1)
y = df_clean.r_squared >= ZCUT

# logistic regression first
from sklearn import linear_model
est = linear_model.LogisticRegression()
est.fit(X, y)

train_pred = est.predict(X)
train_error = sum(train_pred ^ y) / float(len(y))

print train_error
weights = pd.DataFrame(index=X.columns)
weights['val'] = est.coef_[0]
print weights

# looks like the


from sklearn import svm
# do svm with linear kernel to find weights of features so we can
# see what is useful in seeing what users have Zipfian fits
est2 = svm.SVC(kernel='linear')
est2.fit(X, y)

train_pred2 = est2.predict(X)
train_error2 = sum(train_pred2 ^ y) / float(len(y))


print est2.coef_

pickle.dump([est, est2], open('classifiers.p', 'wb'))



# df_vis = df.loc[df.index != df['followers_count'].argmax()]

# from ggplot import *

# ggplot(aes('favourites_count'),
#     data=df_vis) + geom_boxplot() + facet_wrap('zipf')

# # boxplot of r-squared
# print ggplot(df, aes('r_squared')) + geom_boxplot()
# # take out outlier for vis
# print ggplot(df_vis, aes('followers_count')) + geom_boxplot()
# print ggplot(df, aes('statuses_count', 'r_squared')) + \
#     geom_point()

# df_quant = df[['num_fit', 'r_squared', 'slope',
#     'intercept', 'statuses_count', 'followers_count',
#     'following_count', 'age_days', 'favourites_count']].astype(float)
# # correlation needs to be all floats
# corr = df_quant.corr()

# # log and then calculate correlations
# df_quantlog = np.log(df_quant)
# corr2 = df_quantlog.corr()


# df['zipf'] = df.r_squared >= 0.96

