#!/usr/bin/env python
# coding: utf-8

# # Collaborative Filtering

import pandas as pd
from surprise import Reader, Dataset, SVD, SVDpp, SlopeOne, NMF, NormalPredictor, KNNBaseline, KNNBasic, KNNWithMeans, KNNWithZScore, BaselineOnly, CoClustering
from surprise.model_selection import cross_validate, train_test_split
from surprise import accuracy
from surprise.accuracy import rmse
from flask import Flask, render_template, jsonify
import pymongo
import warnings
warnings.filterwarnings("ignore")


# connoct to your Mongo DB database
client = pymongo.MongoClient(
    "mongodb+srv://rishi:rishi@cluster0.mhdj6.mongodb.net/recom?retryWrites=true&w=majority")

# client = pymongo.MongoClient(
#     "localhost", 27017)

# get the database name
db = client.get_database('recom')
# get the particular collection that contains the data
users = db.users
likes = db.likes
posts = db.posts


df_posts = pd.DataFrame(list(posts.find()))
df_users = pd.DataFrame(list(users.find()))
df_views = pd.DataFrame(list(likes.find()))
# df_posts['_id'] = df_posts['_id'].astype(str)
# df_users['_id'] = df_users['_id'].astype(str)
# df_views['_id'] = df_views['_id'].astype(str)


df_posts.rename(columns={'_id': 'post_id',
                ' post_type': 'post_type'}, inplace=True)
df_users.rename(columns={'_id': 'user_id'}, inplace=True)
df_posts.category = df_posts.category.fillna('')

df_merged = pd.merge(df_views, df_users, on='user_id')
df_merged = pd.merge(df_merged, df_posts, on='post_id')

df_merged.drop(columns='timestamp', inplace=True)
df_merged.head()


# print(df_posts.post_type.unique())
# print(df_users.gender.unique())
# print(df_users.academics.unique())


# assigning weights/ranks to different dependencies
w1 = {'skill': 4.1, 'project': 3, 'artwork': 2.1, 'blog': 0.9}
w2 = {'male': 3.1, 'female': 2.5, 'undefined': 1.5}
w3 = {'graduate': 4, 'undergraduate': 3, 'undefined': 1.5}

df_merged['strength'] = ((df_merged['post_type'].apply(lambda x: w1[x]))/4.1 + (
    df_merged['gender'].apply(lambda x: w2[x]))/3.1 + (df_merged['academics'].apply(lambda x: w3[x]))/4)/3
df_merged['strength'] = 5 * \
    (df_merged['strength'].values/max(df_merged['strength'].values))

df_merged = df_merged[['user_id', 'post_id', 'strength']]
df_merged.head()


reader = Reader()
data = Dataset.load_from_df(df_merged, reader)
bestAlgo = []

for algo in [SVD(), SVDpp(), SlopeOne(), NMF(), NormalPredictor(), KNNBaseline(), KNNBasic(), KNNWithMeans(), KNNWithZScore(), BaselineOnly(), CoClustering()]:
    result = cross_validate(algo, data, measures=[
                            'RMSE', 'MAE'], cv=5, verbose=1)
    temp = pd.DataFrame.from_dict(result).mean(axis=0)
    temp = temp.append(
        pd.Series([str(algo).split(' ')[0].split('.')[-1]], index=['Algorithm']))
    bestAlgo.append(temp)


final = pd.DataFrame(bestAlgo).sort_values('test_rmse').set_index('Algorithm')
final


# although all these parameters have some default values. Refer documentation
# other names are pearson_baseline, msd
# 'user_based': True means perform user based recommendation, false means do item based recommendation
sim_options = {'name': 'cosine', 'user_based': True, 'shrinkage': 0}

# Using Alternating Least Squares (ALS)
# reg_u, reg_i = regularization parameter for users and items
bsl_optionsA = {'method': 'als', 'reg_u': 15, 'reg_i': 5, 'n_epochs': 20}
# Using Stochastic Gradient Descent (SGD)
bsl_optionsS = {'method': 'sgd', 'reg': 0.02,
                'learning_rate': .00005, 'n_epochs': 20}

algoA = KNNWithMeans(sim_options=sim_options, bsl_options=bsl_optionsA)
algoS = KNNWithMeans(sim_options=sim_options, bsl_options=bsl_optionsS)

print('ALS-------------------------------------------------------------------------------------------------------------')
cross_validate(algoA, data, measures=['RMSE', 'MAE'], cv=5, verbose=True)
print('SGD-------------------------------------------------------------------------------------------------------------')
cross_validate(algoS, data, measures=['RMSE', 'MAE'], cv=5, verbose=True)


train, test = train_test_split(data, test_size=0.2, random_state=200)
algo = KNNWithMeans(algo=KNNWithMeans(
    sim_options=sim_options, bsl_options=bsl_optionsA))
prediction = algo.fit(train).test(test)
accuracy.rmse(prediction)


def getU(ruid):
    try:
        return len(train.ur[train.to_inner_uid(ruid)])
    except ValueError:  # User id is not a part of trainset
        return 0


def getI(riid):
    try:
        return len(train.ir[train.to_inner_iid(riid)])
    except ValueError:  # Item id is not a part of trainset
        return 0


df_new = pd.DataFrame(prediction, columns=[
                      'user_id', 'post_id', 'rui', 'est', 'details'])
df_new['no_item_rated_by_user'] = df_new.user_id.apply(getU)
df_new['no_user_rated_item'] = df_new.post_id.apply(getI)
df_new['errors'] = abs(df_new.est - df_new.rui)
df_new.head()


bestPred = df_new.sort_values(by='errors')
worstPred = df_new.sort_values(by='errors', ascending=False)


bestPred.head()


worstPred.head()


df_new = pd.merge(df_new, df_posts, on='post_id')
df_new = df_new[['user_id', 'post_id', 'title',
                 'category', 'post_type', 'rui', 'est', 'errors']]
df_new.head()


df_new[df_new['user_id'] == df_new.user_id.value_counts().index[0]
       ].sort_values(by='errors').head()


df_test = pd.DataFrame(test, columns=['user_id', 'post_id', 'merged'])
df_test


def recommend(user_id, n=45):
    res = pd.DataFrame(columns=['user_id', 'post_id', 'estimate'])
    for i in df_test.post_id.unique():
        temp = pd.DataFrame([[user_id, i, algo.predict(user_id, i)[3]]], columns=[
                            'user_id', 'post_id', 'estimate'])
        res = res.append(temp, ignore_index=True)
    res = pd.merge(res, df_posts, on='post_id')
    result = res.sort_values(by='estimate',
                             ascending=False).reset_index(drop=True)[:n].to_json(orient='records')

    return result


# ### Final Recommendation


# recommend('5e4ce251f5561b1994c8e40d')
