#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jun  4 16:02:15 2021

@author: ilegra
"""
'''
from os import path
from time import time
from datetime import datetime


hostname = '54.232.47.179'
database = 'imdb'
database_auth_file = '/database_authentication.txt'
auth_path = '/authentications'
top_actors_file = '/top_actors_file.csv' 
output_path = '/output'
datasets_path = '/datasets'

name_basics_file = 'name.basics.tsv'
title_basics_file = 'title.basics.tsv'
title_principals_file = 'title.principals.tsv'

start_year_col = 'startYear'
title_const_col = 'tconst'
title_type_col = 'titleType'
category_col = 'category'
name_const_col = 'nconst'
primary_name_col = 'primaryName'
primary_profession_col = 'primaryProfession'

id_col = 'ID'
performed_col = 'Performed'
name_col = 'Name'
profession_col = 'Professions'

cols_title_basics = [title_const_col, 
                     start_year_col,
                     title_type_col]

cols_title_principals = [title_const_col, 
                         name_const_col, 
                         category_col]

cols_name_basics = [name_const_col,
                    primary_name_col,
                    primary_profession_col]

actor_quantity = 10
range_year = 10

files_path = path.dirname(path.realpath(__file__))

def import_datasets(file, cols):
    df = read_csv(files_path + datasets_path + '/' + file, 
                  sep = '\t', 
                  header = 0, 
                  usecols = cols,
                  low_memory = False)
    return df.fillna('')


def filter_df_title(filter_lst):
    print(f'Importing and Filtering {title_basics_file} Dataframe...') 
    df = import_datasets(title_basics_file, cols_title_basics)
    df = df[df[start_year_col].isin(filter_lst)]
    df = df[df[title_type_col].str.strip().str.upper() == 'MOVIE']
    print(f'{title_basics_file} Dataframe was filtered.')
    return df


def filter_df_title_principals(filter_lst):
    print(f'Filtering {title_principals_file} Dataframe...')
    df = import_datasets(title_principals_file, cols_title_principals)
    df = df[df[title_const_col].isin(filter_lst)]
    df = df[(df[category_col].str.upper().str.find('ACTOR') != -1) | 
            (df[category_col].str.upper().str.find('ACTRESS') != -1)]
    df = df.groupby([name_const_col, 
                     category_col]).size().reset_index(name = performed_col)
    df.sort_values(by = performed_col, 
                   ascending = False, 
                   inplace = True)
    print(f'{title_principals_file} Dataframe was filtered.')
    return df.head(actor_quantity)

def filter_df_name(filter_lst):
    print(f'Filtering {name_basics_file} Dataframe...')
    df = import_datasets(name_basics_file, cols_name_basics)
    df = df[df[name_const_col].isin(filter_lst)]
    print(f'{name_basics_file} Dataframe was filtered.')
    return df



def main():    
    

    year_lst = [str(datetime.today().year - i) for i in range(range_year)]
    df_title = filter_df_title(year_lst)

 
    title_lst = df_title[title_const_col].to_list()
    df_title_principals = filter_df_title_principals(title_lst)
    
    
    name_lst = df_title_principals[name_const_col].to_list()
    df_name = filter_df_name(name_lst)   
    
    df = merge(df_title_principals,
               df_name, 
               on = name_const_col)
    
    df.rename(columns={name_const_col: id_col, 
                       category_col: category_col.capitalize(),
                       primary_name_col: name_col,
                       primary_profession_col: profession_col}, inplace = True)
    
    df.to_csv(files_path + output_path + top_actors_file, 
              sep = ';',
              index = False, 
              header = True)

start_time = time()
main()
print('Execution time in seconds: ' + str(time() - start_time))
'''
import boto3

session = boto3.Session()
credentials = session.get_credentials()
print(credentials)
