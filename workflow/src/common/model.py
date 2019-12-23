#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sqlalchemy
from sqlalchemy.orm import scoped_session, sessionmaker, mapper
#from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, MetaData, Table, types
from datetime import datetime

class OhayouTime(object):
	pass

class Tweet(object):
	pass

class RetQueue(object):
	pass

class Reply(object):
    pass

init = False
#Base = declarative_base()

metadata = sqlalchemy.MetaData()

ohayouTime = Table("ohayouTime",metadata,
				Column('id', types.Integer, primary_key=True),
				Column('user', types.Unicode(32)),
				Column('type', types.Unicode(32)),
				Column('datetime', types.DateTime, default=datetime.now),
				mysql_engine = 'MyISAM',
				mysql_charset = 'utf8mb4'
				)

# 応答キュー。順番固定
retQueue = Table("retQueue",metadata,
					Column('id', types.Integer, primary_key=True),
					Column('user', types.Unicode(32)),
					Column('text', types.Unicode(140)),
                    Column('reply_id', types.BigInteger(), default=0),
					mysql_engine = 'MyISAM',
					mysql_charset = 'utf8mb4'
			)


tweet = Table("tweet",metadata,
				Column('id', types.Integer, primary_key=True),
				Column('user', types.Unicode(32)),
				Column('text', types.Unicode(140)),
				Column('datetime', types.DateTime, default=datetime.now),
				Column('replyID', types.String(64), default=-1),
				Column('isAnalyze', types.SmallInteger, default=False),
                Column('tweetID', types.BigInteger),
				mysql_engine = 'InnoDB',
				mysql_charset = 'utf8mb4'
			)


reply = Table("reply",metadata,
                Column('id', types.Integer, primary_key=True),
                Column('tweet_id', types.BigInteger),
                Column('reply_text', types.Text),
                Column('src_id', types.BigInteger),
                Column('src_text', types.Text),
                Column('is_analyze', types.SmallInteger, default=False),
                mysql_engine = 'InnoDB',
                mysql_charset = 'utf8mb4'
            )


def startSession(conf):
    global init
    config = {
        "sqlalchemy.url":\
        "mysql+pymysql://"+conf["dbuser"]+":"+conf["dbpass"]+"@"+conf["dbhost"]+"/"+\
        conf["db"]+"?charset=utf8mb4",
        "sqlalchemy.echo":"False"
        }
    engine = sqlalchemy.engine_from_config(config)

    dbSession = scoped_session(
                    sessionmaker(
                        autoflush = True,
                        autocommit = False,
                        bind = engine
                    )
                )

    if init == False:
        mapper(Tweet, tweet)
        mapper(RetQueue, retQueue)
        mapper(OhayouTime, ohayouTime)
        mapper(Reply, reply)
        init = True
    metadata.create_all(bind=engine)
    print ("--start DB Session--")
    return dbSession
		
"""
# テスト内容
a = startSession()
>>> --start DB Session--
"""	
