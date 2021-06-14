#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jun 10 10:53:32 2021

@author: ilegra
"""
import subprocess
from os import path

files_path = path.dirname(path.realpath(__file__))

name_basics_url = ' https://datasets.imdbws.com/name.basics.tsv.gz'
title_basics_url = ' https://datasets.imdbws.com/title.basics.tsv.gz'
title_principals_url = ' https://datasets.imdbws.com/title.principals.tsv.gz'
url_lst = [name_basics_url, title_basics_url, title_principals_url]

name_basics_path = '/datasets/name.basics/'
title_basics_path = '/datasets/title.basics/'
title_principals_path = '/datasets/title.principals/'
path_lst = [name_basics_path, title_basics_path, title_principals_path]

name_basics_file = 'name.basics.tsv.gz'
title_basics_file = 'title.basics.tsv.gz'
title_principals_file = 'title.principals.tsv.gz'
file_lst = [name_basics_file, title_basics_file, title_principals_file]

def download_datasets():
    print('Downloading datasets...')
    
    subprocess.call('rm -rf datasets', shell=True)
    subprocess.call('mkdir datasets', shell=True)
    for index in range(3):
        subprocess.call('wget -P ' + files_path + path_lst[index] + url_lst[index], shell = True)
    
    print('Datasets download was completed.')
        
def unzip_datasets():
    print('Decompressing datasets...')
    
    for index in range(3):
        subprocess.call('gunzip ' + files_path + path_lst[index] + file_lst[index], shell = True)
        
    print('Datasets decompress was completed.')


download_datasets()
unzip_datasets()
