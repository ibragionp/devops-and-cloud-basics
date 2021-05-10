#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri May  7 17:05:37 2021

@author: ilegra
"""

import os
import tweepy as tw
import pandas as pd

api_auth_file = '/api_authentication.txt'

consumer_key= 'yourkeyhere'
consumer_secret= 'yourkeyhere'
access_token= 'yourkeyhere'
access_token_secret= 'yourkeyhere'

def api_connection():
    print(f'Connecting to Twitter API...')
    file = open (path + api_auth_file, 'r')
    lines = file.readlines()
    consumer_key = lines[0].strip()
    consumer_secret = lines[1].strip()
    access_token = lines[2].strip()
    access_token_secret = lines[3].strip()
    file.close()
    auth = tw.OAuthHandler(consumer_key,
                           consumer_secret)
    auth.set_access_token(access_token, 
                          access_token_secret)
    api = tw.API(auth, 
                 wait_on_rate_limit = True)
    print(f'API was connected.')
    return api

def search_tweets_by_name(name, date_since, quantity):
    api = api_connection()
    tweets = tw.Cursor(api.search,
                       q = name,
                       since = date_since).items(quantity)
    
    tweets_lst = [[] for tweet in tweets]

    df_tweets = pd.DataFrame(data = tweets_lst, 
                              columns=['user', "location"])
    
def main():
    