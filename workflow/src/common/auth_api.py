#!/usr/bin/env python
# -*- coding:utf-8 -*-
import json
import tweepy
import sys
import locale
import datetime


locale.setlocale(locale.LC_CTYPE, "")
def load_json(filename):
    f = open(filename)
    result = json.loads(f.read())
    f.close()
    #print filename
    return result


def init_config(consumer_token, consumer_secret,exec_path):

    auth = tweepy.OAuthHandler(consumer_token, consumer_secret)

    try:
        redirect_url = auth.get_authorization_url()
        print(redirect_url)
    except tweepy.TweepError:
        print('Error! Failed to get request token.')
        sys.exit()

    verifier = input('Verifier:').strip()

    auth.get_access_token(verifier)
    print(auth.access_token)
    user = {}
    user["key"] = key = auth.access_token
    user["secret"] = secret = auth.access_token_secret
    user["credential"] = dict(user = tweepy.API(auth).me().screen_name)

    f = open(exec_path + "/user.json", "w")
    json.dump( user, f )
    f.close()
    return user


def connect(consumer_token, consumer_secret, exec_path = "."):
    try:
        user = load_json(exec_path+"/user.json")
    except IOError:
        user = init_config(consumer_token, consumer_secret, exec_path)

    auth = tweepy.OAuthHandler(consumer_token, consumer_secret)
    auth.set_access_token(user["key"], user["secret"])

    api = tweepy.API(auth)
    return api

if __name__ == "__main__":
    conf = load_json("config.json")
    api = connect(conf["consumer_token"], conf["consumer_secret"])
    for s in api.home_timeline():
        print(s.author.screen_name, s.text, s.created_at + \
         datetime.timedelta(hours = 9))
