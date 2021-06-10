#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri May  7 17:05:37 2021

@author: ilegra
"""

import os
from tweepy import OAuthHandler, API, Cursor
from pandas import read_csv, DataFrame, concat
from smart_open import smart_open
import time

with smart_open('s3://jt-dataeng-isabellabragionpereira/tema09/api_authentication/api_authentication.txt', 'rb') as s3_source:
    for line in s3_source:
         print(line.decode('utf8'))


api_auth_file = '/api_authentication.txt'
top_actors_file = '/top_actors_file.csv' 
top_actors_tweets_file = '/top_actors_tweets_file.csv'
auth_path = '/authentications'
output_path = '/output'

name_col = 'Name'
actor_actress_col = 'Actor/actress name'

date_since = '2010-01-01'
quantity = 10

path = os.path.dirname(os.path.realpath(__file__))

with smart_open('s3://jt-dataeng-isabellabragionpereira/tema09/api_authentication/api_authentication.txt', 'rb') as s3_source:
    lines = s3_source.readlines()
    print(lines)
    
'''
    for line in s3_source:
         print(line.decode('utf8'))

    s3_source.seek(0)  # seek to the beginning
    b1000 = s3_source.read(1000)  # read 1000 bytes



def api_connection():
    print(f'Connecting to Twitter API...')
    file = open (path + auth_path + api_auth_file, 'r')
    lines = file.readlines()
    consumer_key = lines[0].strip()
    consumer_secret = lines[1].strip()
    access_token = lines[2].strip()
    access_token_secret = lines[3].strip()
    file.close()
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
'''