#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import os

# /home/*/hama_dbとかが返ってくる
#exec_path = os.path.abspath(os.path.dirname(__file__)).rsplit("/",1)[0]
exec_path = "."
conf_path = exec_path+"/common/config.json"
sys.path.insert(0,exec_path)
from common import auth_api, model

import json
import datetime
from   sqlalchemy import and_
import random

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
        #l = tw.home_timeline(page = page_number, count=100)
        l = tw.search("かすかす", count=10)
        page_number += 1
        if page_number > 2: break
        for s in l:
            if( s.text.startswith("RT ")): continue
            print("rep: ", s.in_reply_to_status_id)
            if( s.in_reply_to_status_id is not None and\
                int(s.in_reply_to_status_id) != -1 and\
                not(s.text.startswith("@NakasukasumiB")))): continue
            #if s.author.screen_name == userdata["user"]:continue
            
            jTime = s.created_at + datetime.timedelta(hours = 9)
            name = s.user.screen_name
            if( is_ng_user(name) ): continue
            query = dbSession.query(model.Tweet).filter(
                and_(
                    model.Tweet.user==name,
                    model.Tweet.tweetID == s.id
                )
            )
            if( query.count() > 0 ): continue
            update_flag = True

            t = model.Tweet()
            t.user = name
            t.text = s.text
            t.datetime = jTime
            t.replyID = s.in_reply_to_status_id
            t.tweetID = s.id
            #print "id:",s.id, 
            dbSession.add(t)

            message =""
            if(s.text.startswith("@NakasukasumiB")):
                message = random.choice([
                    "せんぱい、コッペパン焼いてきましたよ！", 
                    "えへへっ！"
                ])
            else:
                message = random.choice([
                    "かすかすじゃなくってかすみんです！",
                    "かすみん！",
                    "だから、かすかすじゃなくってかすみんですってば！"
                ])
            tw.update_status("@"+name+" "+message, t.replyID)
        dbSession.commit()


if __name__ == "__main__":
    main()
