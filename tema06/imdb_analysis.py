#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon May  3 08:31:15 2021

@author: ilegra
"""
from pandas import concat, merge
from os import path
from time import time
from datetime import datetime
from pandas.io.sql import read_sql
import mysql.connector as sql


hostname = '54.232.47.179'
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
primary_profession_col = 'primaryProfession'

id_col = 'ID'
performed_col = 'Performed'
name_col = 'Name'
profession_col = 'Professions'

actor_quantity = 10
range_year = 10

path = path.dirname(path.realpath(__file__))

def database_connection():
    print(f'Connecting to {database} database...')
    file = open (path + auth_path + database_auth_file, 'r')
    lines = file.readlines()
    user = lines[0].strip()
    password = lines[1].strip()
    file.close()
    db_connection = sql.connect(host = hostname, 
                                database = database, 
                                user = user,
                                password = password)
    print(f'{database} database was connected.')
    return db_connection


def filter_df_title(df, tb):
    print(f'Filtering {title_basics_tb} Dataframe...') 
    df = df[df[title_type_col].str.strip().str.upper() == 'MOVIE']
    print(f'{title_basics_tb} Dataframe was filtered.')
    return df


def filter_df_title_principals(df):
    print(f'Filtering {title_principals_tb} Dataframe...')
    df = df.groupby([name_const_col, 
                     category_col]).size().reset_index(name = performed_col)
    df.sort_values(by = performed_col, 
                    ascending = False, 
                    inplace = True)
    print(f'{title_principals_tb} Dataframe was filtered.')
    return df.head(actor_quantity)


def filter_df_by_profession(df, tb):
    print(f'Filtering Dataframe by profession...')
    col = category_col
    if tb == name_basics_tb:
        col = primary_profession_col
    df = df[(df[col].str.upper().str.find('ACTOR') != -1) | 
            (df[col].str.upper().str.find('ACTRESS') != -1)]
    print(f'Dataframe was filtered.')
    return df
        

def create_lst_str(col_lst):
    col_lst_str = ", ".join([f"'{col}'" for col in col_lst])
    return col_lst_str


def import_data_from_database(tb, cols_select, col_where, values_where_in, col_pk, func):
    chunk_size = 10000
    offset = 0
    db_connection = database_connection()
    dfs = []
    while True:
      sql = "SELECT %s FROM %s WHERE %s IN (%s) ORDER BY %s LIMIT %d OFFSET %d" % (cols_select,
                                                                                 tb,
                                                                                 col_where,
                                                                                 values_where_in,
                                                                                 col_pk,
                                                                                 chunk_size,
                                                                                 offset)
      df_result = read_sql(sql, db_connection)
      if not df_result.empty:
          dfs.append(func(df_result, tb))
          offset += chunk_size
      else:
        break
    full_df = concat(dfs)
    db_connection.close()
    return full_df


def main():    
    
    cols_select_title_basics = ', '.join([title_const_col, 
                                        start_year_col, 
                                        title_type_col])
    year_lst = [datetime.today().year - i for i in range(range_year)]
    values_where_in_title_basics = create_lst_str(year_lst)
    df_title = import_data_from_database(title_basics_tb, 
                                         cols_select_title_basics,
                                         start_year_col, 
                                         values_where_in_title_basics,
                                         title_const_col,
                                         filter_df_title)


    cols_select_title_principals = ', '.join([title_const_col, 
                                              name_const_col, 
                                              category_col])    
    values_where_in_title_principals = create_lst_str(df_title[title_const_col].to_list())
    df_title_principals = import_data_from_database(title_principals_tb, 
                                              cols_select_title_principals,
                                              title_const_col,
                                              values_where_in_title_principals,
                                              title_const_col,
                                              filter_df_by_profession)
    df_title_principals = filter_df_title_principals(df_title_principals)
    
    
    cols_select_name = ', '.join([name_const_col,
                                  primary_name_col,
                                  primary_profession_col])
    values_where_in_name = create_lst_str(df_title_principals[name_const_col].to_list())
    df_name = import_data_from_database(name_basics_tb, 
                                        cols_select_name,
                                        name_const_col,
                                        values_where_in_name,
                                        name_const_col,
                                        filter_df_by_profession)   
    
    df = merge(df_title_principals,
                  df_name, 
                  on = name_const_col)
    
    df.rename(columns={name_const_col: id_col, 
                       category_col: category_col.capitalize(),
                       primary_name_col: name_col,
                       primary_profession_col: profession_col}, inplace = True)
    
    df.to_csv(path + output_path + top_actors_file, 
              sep = ';',
              index = False, 
              header = True)

start_time = time()
main()
print('Execution time in seconds: ' + str(time() - start_time))
