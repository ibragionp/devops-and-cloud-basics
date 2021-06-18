FROM python:3
RUN pip install awscli
RUN mkdir /tema10
WORKDIR /tema10
RUN pip install datetime
RUN pip install pandas
RUN pip install boto3
RUN pip install tweepy
COPY /tema06 /tema10/
CMD ["main.py"]
ENTRYPOINT ["python3"]
