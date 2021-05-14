#!/bin/sh
# Sync ec2-user to Bucket S3
aws s3 --region us-east-2 sync jt-dataeng-isabella/imdb/output/ s3://jt-dataeng-isabellabragionpereira/tema07/output/
