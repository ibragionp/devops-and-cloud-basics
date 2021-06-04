#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jun  4 10:40:12 2021

@author: ilegra
"""

'''

from botocore.credentials import InstanceMetadataProvider, InstanceMetadataFetcher

provider = InstanceMetadataProvider(iam_role_fetcher=InstanceMetadataFetcher(timeout=1000, num_attempts=2))
credentials = provider.load()


access_key = credentials.access_key
secret_key = credentials.secret_key

print(access_key)
print(secret_key)
'''
'''
import boto3

session = boto3.Session()
credentials = session.get_credentials()

credentials = credentials.get_frozen_credentials()

ACCESS_KEY = credentials.access_key
SECRET_KEY = credentials.secret_key

print(ACCESS_KEY)
print(SECRET_KEY)
'''

from botocore.utils import InstanceMetadataFetcher
from botocore.credentials import InstanceMetadataProvider
provider = InstanceMetadataProvider(iam_role_fetcher=InstanceMetadataFetcher(timeout=1000, num_attempts=2))
creds = provider.load()
print(creds.access_key)
print(creds.secret_key)