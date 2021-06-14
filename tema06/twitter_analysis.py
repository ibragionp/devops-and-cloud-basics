#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri May  7 17:05:37 2021

@author: ilegra
"""

import os
from tweepy import OAuthHandler, API, Cursor
from pandas import read_csv, DataFrame, concat
import time
import boto3

bucket_api_auth = 'jt-dataeng-isabellabragionpereira'
key_api_auth = 'tema09/api_authentication/api_authentication.txt'
top_actors_file = '/top_actors_file.csv' 
top_actors_tweets_file = '/top_actors_tweets_file.csv'
output_path = '/output'
api_auth_file = '/api_authentication.txt'
  
name_col = 'Name'
actor_actress_col = 'Actor/actress name'

date_since = '2010-01-01'
quantity = 10
'''
from boto3 import Session

session = Session()
credentials = session.get_credentials()
print(credentials)
# Credentials are refreshable, so accessing your access key / secret key
# separately can lead to a race condition. Use this to get an actual matched
# set.
current_credentials = credentials.get_frozen_credentials()

# I would not recommend actually printing these. Generally unsafe.
print(current_credentials.access_key)
print(current_credentials.secret_key)
print(current_credentials.token)
'''
path = os.path.dirname(os.path.realpath(__file__))

def api_connection():
    print(f'Connecting to Twitter API...')
    
    s3 = boto3.resource('s3')
    content_object = s3.Object(bucket_name=bucket_api_auth, key=key_api_auth)
    file_content = content_object.get()['Body'].read().decode('utf-8')
    lines = file_content.split('\n')
    consumer_key = lines[0].strip()
    consumer_secret = lines[1].strip()
    access_token = lines[2].strip()
    access_token_secret = lines[3].strip()
    auth = OAuthHandler(consumer_key,
                        consumer_secret)
    auth.set_access_token(access_token, 
                          access_token_secret)
    api = API(auth, 
                 wait_on_rate_limit = True)
    
    print(f'API was connected.')
    return api

def import_csv():
    print(f'Import csv file {top_actors_file} to DataFrame...')
    df = read_csv(path + output_path + top_actors_file,
                     sep = ';',
                     header = 0,
                     usecols = [name_col])
    print(f'The csv file {top_actors_file} was imported.')
    return df
    

def search_tweets_by_name(name, api):
    print(f'Searching tweets information name: {name}...')
    tweets = Cursor(api.search,
                       q = name,
                       since = date_since).items(quantity)
    
    tweets_lst = [[tweet.id, 
                   tweet.text,
                   tweet.user.screen_name,
                   tweet.user.name, 
                   tweet.lang,
                   tweet.created_at] for tweet in tweets]

    df_tweets = DataFrame(tweets_lst, columns = ['ID', 
                                                    'Text',
                                                    'Username',
                                                    'Name',
                                                    'Language',
                                                    'Created at'])
    df_tweets[actor_actress_col] = name
    
    print(f'Tweets were searched.')
    return df_tweets
    
def main():
    
    api = api_connection()
    df_primary_name = import_csv()
    
    appended_df = []
    
    for index, row in df_primary_name.iterrows():
        df = search_tweets_by_name(row[name_col], api)
        appended_df.append(df)
    
    appended_df = concat(appended_df)
    
    appended_df.to_csv(path + output_path + top_actors_tweets_file, 
                       sep = ';',
                       index = False, 
                       header = True)

start_time = time.time()
main()
print('Execution time in seconds: ' + str(time.time() - start_time))
