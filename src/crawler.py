#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import os
import json
import datetime
from   sqlalchemy import and_
import random

# /home/*/hama_dbとかが返ってくる
#exec_path = os.path.abspath(os.path.dirname(__file__)).rsplit("/",1)[0]
exec_path = "."
conf_path = exec_path+"/common/config.json"
sys.path.insert(0,exec_path)
from common import auth_api, model
import tweepy


#ログに入れない人のリスト
g_ngUser = [ 
	"NakasukasumiB" 
]


dbSession = None


def get_auth_data(fileName):
	file = open(fileName,'r')
	a = json.loads(file.read())
	file.close()
	return a


# NGUserならTrue そうでないならFalse 
def is_ng_user(user):
    for u in g_ngUser:
        if u == user: return True
    return False


def check_reply(reply_id):
    if(reply_id is not None and\
        int(reply_id) != -1):
        return False
    return True


def check_none(reply_id):
    return True


"""
    テキストが適合している = True
    重複してたり、RTだったり = False
"""
def check_text(text, reply_id, name, created_at, id, dbSession, check_func):
    if( text.startswith("RT ")): return False
    print("rep: ", reply_id)
    if(not(check_func(reply_id))): return False
    #if s.author.screen_name == userdata["user"]:continue
            
    jTime = created_at + datetime.timedelta(hours = 9)
    if( is_ng_user(name) ): return False
    query = dbSession.query(model.Tweet).filter(
        and_(
            model.Tweet.user==name,
            model.Tweet.tweetID == id
        )
    )
    if( query.count() > 0 ): return False
    t = model.Tweet()
    t.user = name
    t.text = text
    t.datetime = jTime
    t.replyID = reply_id
    t.tweetID = id
    dbSession.add(t)
    return True


def main():

    # twitterから発言を取ってきてDBに格納する
    userdata = get_auth_data(conf_path)
    tw = auth_api.connect(userdata["consumer_token"],
        userdata["consumer_secret"], exec_path+"/common/")
    #print tw.rate_limit_status()
    dbSession = model.startSession(userdata)

    page_number = 0
    update_flag = True
    while update_flag:
        update_flag = False
        page_number += 1
        if page_number > 2: break

        l = tw.search("かすかす", count=10)
        for s in l:
            update_flag = check_text(s.text, s.in_reply_to_status_id,
                    s.user.screen_name, s.created_at,
                    s.id, dbSession, check_reply)
            if(not(update_flag)): continue
            message = random.choice([
                "かすかすじゃなくってかすみんです！",
                "かすみん！",
                "だから、かすかすじゃなくってかすみんですってば！"
            ])
            try:
                tw.update_status("@"+s.user.screen_name+" "+message, s.in_reply_to_status_id)
            except tweepy.TweepError:
                pass
        dbSession.commit()
        
    page_number = 0
    update_flag = True
    while update_flag:
        update_flag = False
        page_number += 1
        if page_number > 2: break

        l = tw.search("@NakasukasumiB", count=10)
        for s in l:
            update_flag = check_text(s.text, s.in_reply_to_status_id,
                    s.user.screen_name, s.created_at,
                    s.id, dbSession, check_none)
            if(not(update_flag)): continue
            print("user: "+s.user.screen_name)
            message = random.choice([
                "せんぱい、コッペパン焼いてきましたよ！", 
                "えへへっ！"
            ])
            try:
                tw.update_status("@"+s.user.screen_name+" "+message, s.in_reply_to_status_id)
            except tweepy.TweepError:
                pass
        dbSession.commit()


if __name__ == "__main__":
    main()
