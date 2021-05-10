#!/usr/bin/env python3
# -*- coding: utf-8 -*-
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
import datetime

hostname = '54.94.212.147'
database = 'imdb'
database_auth_file = '/database_authentication.txt'
auth_path = '/authentications'
top_actors_file = '/top_actors_file.csv' 
output_path = '/output'

name_basics_tb = 'name_basics'
title_basics_tb = 'title_basics'
title_principals_tb = 'title_principals'

start_year_col = 'startYear'
title_const_col = 'tconst'
title_type_col = 'titleType'
category_col = 'category'
name_const_col = 'nconst'
primary_name_col = 'primaryName'

id_col = 'ID'
performed_col = 'Performed'
name_col = 'Name'

actor_quantity = 10
range_year = 10

path = os.getcwd()

def database_connection():
    print(f'Connecting to {database} database...')
    file = open (path + auth_path + database_auth_file, 'r')
    lines = file.readlines()
    user = lines[0].strip()
    password = lines[1].strip()
    file.close()
    db_connection_str = f'mysql+pymysql://{user}:{password}@{hostname}/{database}'
    print(f'{database} database was connected.')
    return create_engine(db_connection_str)


def filter_df_title(df):
    print(f'Filtering {title_basics_tb} Dataframe...') 
    df = df[df[title_type_col].str.strip().str.upper() == 'MOVIE']
    print(f'{title_basics_tb} Dataframe was filtered.')
    return df


def filter_df_title_principals(df):
    print(f'Filtering {title_principals_tb} Dataframe...')
    df = df[(df[category_col].str.upper().str.find('ACTOR') != -1) | 
            (df[category_col].str.upper().str.find('ACTRESS') != -1)]
    df = df.groupby([name_const_col, 
                     category_col]).size().reset_index(name = performed_col)
    df.sort_values(by = performed_col, 
                    ascending = False, 
                    inplace = True)
    print(f'{title_principals_tb} Dataframe was filtered.')
    return df.head(actor_quantity)
        

def create_lst_str(df, col):
    col_lst = df[col].to_list()
    col_lst_str = ", ".join([f"'{item}'" for item in col_lst])
    return col_lst_str


def main():
    
    db_connection = database_connection()
    
    year_lst = [datetime.datetime.today().year - i for i in range(range_year)]
    year_lst_str = ", ".join([f"'{year}'" for year in year_lst])
    df_title = pd.read_sql(f'SELECT {title_const_col}, {start_year_col}, {title_type_col} FROM {title_basics_tb} WHERE {start_year_col} IN ({year_lst_str})', 
                           con = db_connection)
    df_title = filter_df_title(df_title)
    
    title_lst_str = create_lst_str(df_title, title_const_col)
    df_principals = pd.read_sql(f'SELECT {title_const_col}, {name_const_col}, {category_col} FROM {title_principals_tb} WHERE {title_const_col} IN ({title_lst_str})', 
                                con = db_connection)

    df_title_principals = filter_df_title_principals(df_principals)
    
    name_lst_str = create_lst_str(df_title_principals, name_const_col)
    df_name = pd.read_sql(f'SELECT {name_const_col}, {primary_name_col} FROM {name_basics_tb} WHERE {name_const_col} IN ({name_lst_str})', 
                          con = db_connection)
    
    df = pd.merge(df_title_principals,
                  df_name, 
                  on = name_const_col)
    
    df.rename(columns={name_const_col: id_col, 
                       category_col: category_col.capitalize(),
                       primary_name_col: name_col}, inplace = True)
    
    df.to_csv(path + output_path + top_actors_file, 
              sep = ';',
              index = False, 
              header = True)

start_time = time.time()
main()
print('Execution time in seconds: ' + str(time.time() - start_time))