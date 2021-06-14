#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jun 14 16:03:53 2021

@author: ilegra
"""

import os

output_path = '/output'
top_actors_tweets_file = '/top_actors_file.csv'
top_actors_tweets_file = '/top_actors_tweets_file.csv'

files_path = os.path.dirname(os.path.realpath(__file__)) + output_path

def check_file_exists():
    exists = False
    if os.path.isfile(files_path + top_actors_tweets_file) and os.path.isfile(files_path + top_actors_tweets_file):
        exists = True
    return exists

print(check_file_exists())
