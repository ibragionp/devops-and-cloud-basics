#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed May 19 17:10:33 2021

@author: ilegra
"""
from subprocess import Popen, PIPE
import os
#import get_datasets
#import imdb_analysis
import twitter_analysis

path = os.path.dirname(os.path.realpath(__file__))
output_path = '/output'
#sync_aws_str = 'aws s3 sync /var/lib/jenkins/workspace/python-script-pipeline-jenkinsfile/tema06/ s3://jt-dataeng-isabellabragionpereira/tema09/output/'
#sync_aws_str = 'sudo -S su - ec2-user -c "aws s3 sync {path}{output_path} s3://jt-dataeng-isabellabragionpereira/tema09/output/ "'.format(
#        path = path, 
#        output_path = output_path) 
sync_aws_str = 'aws s3 sync {path}{output_path} s3://jt-dataeng-isabellabragionpereira/tema09/output/'.format(
        path = path, 
        output_path = output_path) 
    
def execute_scripts_analysis():
    #get_datasets
    #imdb_analysis
    twitter_analysis
    
def sync_bucket_s3_aws():
    terminal = sync_aws_str
    push = Popen(terminal, shell = True, stdout = PIPE)
    push.wait() 
    print(push.returncode)
 
    
execute_scripts_analysis()
sync_bucket_s3_aws()

