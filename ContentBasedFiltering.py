#!/usr/bin/env python
# coding: utf-8

# # Content Based Recommendation System (Recommending similar posts for given post)


import warnings
from sklearn.metrics.pairwise import linear_kernel, cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
import pandas as pd
import pymongo


warnings.filterwarnings("ignore")

# connoct to your Mongo DB database
client = pymongo.MongoClient(
    "mongodb+srv://rishi:rishi@cluster0.mhdj6.mongodb.net/recom?retryWrites=true&w=majority")

# get the database name
db = client.get_database('recom')
# get the particular collection that contains the data
users = db.users
likes = db.likes
posts = db.posts


# print(list(posts.find()))
df_posts = pd.DataFrame(list(posts.find()))
df_users = pd.DataFrame(list(users.find()))
df_views = pd.DataFrame(list(likes.find()))
df_posts['_id'] = df_posts['_id'].astype(str)
df_users['_id'] = df_users['_id'].astype(str)
df_views['_id'] = df_views['_id'].astype(str)

# print(df_posts["_id"])
# print(df_views.head())


df_posts.rename(columns={'_id': 'post_id',
                ' post_type': 'post_type'}, inplace=True)
df_users.rename(columns={'_id': 'user_id'}, inplace=True)
df_posts.category = df_posts.category.fillna('')
# print(df_posts.head())
# print(df_users.head())


# merging users table with views using user id as key
df_merged = pd.merge(df_views, df_users, on='user_id')
# merging posts table with newly created merged table using post id as key
df_merged = pd.merge(df_merged, df_posts, on='post_id')
df_merged.head()


df_merged.drop(columns='timestamp', inplace=True)
df_merged.head()


# establishing relation between posts using post title, category and type
tf = TfidfVectorizer(analyzer='word', ngram_range=(1, 2),
                     min_df=0, stop_words='english')
tf_matrix1 = tf.fit_transform(df_posts['title'])
tf_matrix2 = tf.fit_transform(df_posts['category'])
tf_matrix3 = tf.fit_transform(df_posts['post_type'])

csm1 = linear_kernel(tf_matrix1, tf_matrix1)
csm2 = linear_kernel(tf_matrix2, tf_matrix2)
csm3 = linear_kernel(tf_matrix3, tf_matrix3)
csm_tf = (csm1 + csm2 + csm3)/3


def cleanData(x):
    if isinstance(x, list):
        return str.lower(x)
    else:
        if isinstance(x, str):
            return str.lower(x)
        else:
            return ''


def combine(x):
    # new columns for algo application and to prevent affecting the original data
    return x['title1'] + ' ' + x['category1'] + ' ' + x['post_type1']


features = ['title', 'category', 'post_type']

for feature in features:
    df_posts[feature + '1'] = df_posts[feature].apply(cleanData)

df_posts['merged'] = df_posts.apply(combine, axis=1)
# df_posts.head()

count = CountVectorizer(stop_words='english')
count_matrix = count.fit_transform(df_posts['merged'])
csm_count = cosine_similarity(count_matrix, count_matrix)
# delete the new columns as processing is done on the merged column
df_posts.drop(columns=['title1', 'category1',
              'post_type1', 'merged'], inplace=True)
# df_posts.drop(columns='post_id', inplace=True)
df_posts.style.set_properties(**{'text-align': 'center'})


# recommmendation function
# df_posts.set_index('title', inplace=True) can also be done to set post title as index column
indices = pd.Series(df_posts.index, index=df_posts.title)

# first we pass csm in the function definition without giving any value. Later, when the function is called, it will be checked for different values of csm for which the function gives the best results.
# That value of csm will then be passed in the function definition, so that csm value isn't needed to be given while calling the function.

# earlier
# def recommend(post, csm):
# later

# choosing this csm as it covers both aspects
# choosing this csm as it covers both aspects


def recom(post, csm=(csm_tf + csm_count)/2):
    idx = indices[post]
    # print(idx)
    score_series = list(enumerate(csm[idx]))
    # print("Score Series::")
    # print(score_series)
    score_series = sorted(score_series, key=lambda x: x[1], reverse=True)
    # not recommending the original post itself, starting from 1
    score_series = score_series[1:20]
    post_indices = [i[0] for i in score_series]
    # print(df_posts.loc[post_indices].to_json(orient='records'))
    return df_posts.loc[post_indices].to_json(orient='records')


# print(csm_tf)
# print(csm_count)
# print((csm_tf + csm_count)/2)


# ### Final recommendation
# recom('Recom Engine')
