#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed May 19 17:10:33 2021

@author: ilegra
"""
import subprocess
import os

path = os.path.dirname(os.path.realpath(__file__))

#exec(open(path + '/imdb_analysis.py').read())
#exec(open(path + '/twitter_analysis.py').read())

cmd = 'aws s3 sync devops-and-cloud-basics/tema06/output/ s3://jt-dataeng-isabellabragionpereira/tema09/output/'
push = subprocess.Popen(cmd, shell = True, stdout = subprocess.PIPE)
push.wait()   # the new line
print(push.returncode)