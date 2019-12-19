FROM python:3.7

LABEL maintainer="Showyou <showyou41@gmail.com>"

ENV LANG=C.UTF-8

RUN apt-get update && apt-get install -y python3-pip && \
    groupadd -r bot && useradd --no-log-init -r -m -g bot bot
USER bot
WORKDIR /home/bot
RUN pip3 install --user pymysql sqlalchemy tweepy
