#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed May 19 17:10:33 2021

@author: ilegra
"""
from subprocess import Popen, PIPE

sync_aws_str = 'aws s3 sync ~/devops-and-cloud-basics/tema06/output/ s3://jt-dataeng-isabellabragionpereira/tema09/output/'
    
def execute_scripts_analysis():
    #exec(open('imdb_analysis.py').read())
    exec(open('twitter_analysis.py').read())
    
def sync_bucket_s3_aws():
    terminal = sync_aws_str
    push = Popen(terminal, shell = True, stdout = PIPE)
    push.wait() 
    print(push.returncode)
 
    
execute_scripts_analysis()
sync_bucket_s3_aws()
