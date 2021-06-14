#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jun 10 10:53:32 2021

@author: ilegra
"""
import os

output_path = '/output'
top_actors_tweets_file = '/top_actors_tweets_file.csv'

files_path = os.path.dirname(os.path.realpath(__file__)) + output_path + top_actors_tweets_file

def check_file_exists():
    exists = False
    if os.path.isfile(files_path):
        exists = True
    return exists

print(check_file_exists())