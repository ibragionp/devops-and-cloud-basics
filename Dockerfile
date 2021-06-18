FROM python:3
ARG AWS_ACCESS_KEY_ID 
ARG AWS_SECRET_ACCESS_KEY
ARG AWS_DEFAULT_REGION=sa-east-1
RUN pip install awscli
ENV AWS_ACCESS_KEY_ID=$AWS_ACCESS_KEY_ID
ENV AWS_SECRET_ACCESS_KEY=$AWS_SECRET_ACCESS_KEY
RUN mkdir /tema10
WORKDIR /tema10
RUN pip install datetime
RUN pip install pandas
RUN pip install boto3
RUN pip install tweepy
COPY /tema06 /tema10/
CMD ["main.py"]
ENTRYPOINT ["python3"]