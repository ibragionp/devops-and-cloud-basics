#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed May 19 17:10:33 2021

@author: ilegra
"""
from subprocess import Popen, PIPE
#import imdb_analysis
import twitter_analysis

#sync_aws_str = 'aws s3 sync /var/lib/jenkins/workspace/python-script-pipeline-jenkinsfile/tema06/ s3://jt-dataeng-isabellabragionpereira/tema09/output/'
sync_aws_str = 'sudo -S su - ec2-user -c "aws s3 sync /home/ec2-user/devops-and-cloud-basics/tema09/output/ s3://jt-dataeng-isabellabragionpereira/tema09/output/ "'
    
def execute_scripts_analysis():
    #imdb_analysis
    twitter_analysis
    
def sync_bucket_s3_aws():
    terminal = sync_aws_str
    push = Popen(terminal, shell = True, stdout = PIPE)
    push.wait() 
    print(push.returncode)
 
    
execute_scripts_analysis()
sync_bucket_s3_aws()
