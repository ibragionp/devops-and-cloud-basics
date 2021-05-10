#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon May  3 08:31:15 2021

@author: ilegra
"""

from sqlalchemy import create_engine

import pandas as pd

import os

import time

hostname = '54.94.212.147'
database = 'imdb'
database_auth_file = '/database_authentication.txt'
top_actors_file = 'top_ten_actors_file.csv' 

name_basics_tb = 'name_basics'
title_basics_tb = 'title_basics'
title_principals_tb = 'title_principals'

start_year_col = 'startYear'
title_const_col = 'tconst'
tile_type_col = 'titleType'
category_col = 'category'
name_const_col = 'nconst'
appearances_col = 'appearances'

path = os.getcwd()

def database_connection():
    print(f'Connecting to {database} database...')
    file = open (path + database_auth_file, 'r')
    lines = file.readlines()
    user = lines[0].strip()
    password = lines[1].strip()
    file.close()
    db_connection_str = f'mysql+pymysql://{user}:{password}@{hostname}/{database}'
    print(f'{database} database was connected.')
    return create_engine(db_connection_str)


def filter_df_na(df, col):
    print('Filtering NaN and empty values...')
    df.fillna('', inplace = True)
    df = df[(df[col].str.upper().str.strip() != 'N') & 
            (df[col].str.strip() != '')]
    print('The Dataframe was filtered.')
    return df


def filter_df_title(df):
    print(f'Filtering {title_basics_tb} Dataframe...')
    df[start_year_col] = df[start_year_col].astype(int, errors = 'ignore'), 
    df = df[(df[start_year_col] >= 2010) & 
            (df[tile_type_col].str.strip().str.upper() == 'MOVIE')]
    print(f'{title_basics_tb} Dataframe was filtered.')
    return df


def filter_df_title_principals(df, title_lst):
    print(f'Filtering {title_principals_tb} Dataframe...')
    df = df[df[title_const_col].str.strip().str.upper().isin(title_lst)]
    df = df[(df[category_col].str.upper().str.find('ACTOR') != -1) | 
            (df[category_col].str.upper().str.find('ACTRESS') != -1)]
    df = df.groupby([name_const_col, 
                     category_col]).size().reset_index(name = appearances_col)
    df.sort_values(by = appearances_col, 
                    ascending = False, 
                    inplace = True)
    print(f'{title_principals_tb} Dataframe was filtered.')
    return df.head(10)
        

def main():
    
    db_connection = database_connection()
    
    df_title = pd.read_sql(f'SELECT tconst, startYear, titleType FROM {title_basics_tb} ORDER BY tconst DESC LIMIT 1000', 
                           con = db_connection)
    
    df_principals = pd.read_sql(f'SELECT {title_const_col}, nconst, category FROM {title_principals_tb} ORDER BY nconst DESC LIMIT 1000', 
                                con = db_connection)

    df_name = pd.read_sql(f'SELECT nconst, primaryName FROM {name_basics_tb} ORDER BY nconst DESC LIMIT 1000', 
                          con = db_connection)

    df_title = filter_df_na(df_title, 
                            start_year_col)
    title_lst = df_title[title_const_col].str.upper().to_list()
    
    df_title_principals = filter_df_title_principals(df_principals, 
                                                     title_lst)
    df = pd.merge(df_title_principals,
                  df_name, 
                  on = name_const_col)
    df.to_csv (path + top_actors_file, 
               index = False, 
               header = True)

start_time = time.time()
main()
print('Execution time in seconds: ' + time.time() - start_time)
