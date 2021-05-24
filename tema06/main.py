#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed May 19 17:10:33 2021

@author: ilegra
"""
from subprocess import Popen, PIPE
from os import path

sync_aws_str = 'aws s3 sync ~/devops-and-cloud-basics/tema06/output/ s3://jt-dataeng-isabellabragionpereira/tema09/output/'
imdb_analysis_file = '/imdb_analysis.py'
twitter_analysis_file = '/twitter_analysis.py'
    
def execute_scripts_analysis():
    files_path = path.dirname(path.realpath(__file__))
    exec(open(files_path + imdb_analysis_file).read())
    exec(open(files_path + twitter_analysis_file).read())

def sync_bucket_s3_aws():
    terminal = sync_aws_str
    push = Popen(terminal, shell = True, stdout = PIPE)
    push.wait() 
    print(push.returncode)
    
execute_scripts_analysis()
sync_bucket_s3_aws()
