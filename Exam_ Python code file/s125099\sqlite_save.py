# -*- coding:utf-8 -*-

import sqlite3
from peewee import BaseModel, CharField, Model, SqliteDatabase

try:
    import config
    # TODO: Fix relative import config is in ../config/config.py
    # and/or move config file
    DATABASE_LOCATION = config.DATABASE_LOCATION
except ImportError:
    DATABASE_LOCATION = 'lite.db'


database = SqliteDatabase(DATABASE_LOCATION)
database.connect()


class BaseModel(Model):
    '''Base class for the models'''
    class Meta:
        database = database


class Tweet(BaseModel):
    '''Model for Tweet table, stores all the information
    that is gathered using the module Pattern's search function'''
    # TODO: Add primary key and index(es)
    # TODO: Move model(s) to separate file
    profile = CharField()
    language = CharField()
    author = CharField()
    url = CharField()
    text = CharField()
    date = CharField()
    tweet_id = CharField()


def generateRowDict(data):
    '''Generator that returns data row as dictionary'''
    for row in data:
        row_dict = {}
        for key, value in row:
            row_dict[key] = value
        yield row_dict


def saveTweets(tweets):
    '''Function that stores tweets in database'''
    # TODO: Nose tests
    for row_dict in generateRowDict(tweets):
        tweet = Tweet()
        tweet.profile = row_dict.get('profile')
        tweet.language = row_dict.get('language')
        tweet.author = row_dict.get('author')
        tweet.url = row_dict.get('url')
        tweet.text = row_dict.get('text')
        tweet.date = row_dict.get('date')
        tweet.tweet_id = row_dict.get('id')
        tweet.save()


def main():
    '''Main function used when running script independently.
    Test data 'tweets' has expected data format'''
    tweets = [[(u'profile',
                u'http://a0.twimg.com/profile_images/2709678005/'
                'e4dfb055e127c9f1f41b90335e67e964_normal.jpeg'),
               (u'language', u'en'),
               (u'author', u'PatrakaarPopat'),
               (u'url', u'https://twitter.com/PatrakaarPopat/status/'
                '385052813715185664'),
               (u'text', u"RT @cpjasia: Journo from #Indonesia wins @AFP"
                "prize for brave reporting on #Syria's civil war and"
                " #Jakarta's drug trade. http://t.co/i0cvBP\u2026"),
               (u'date', u'Tue Oct 01 14:45:19 +0000 2013'),
               (u'id', u'385052813715185664')], ]
    if not Tweet.table_exists():
        Tweet.create_table()
    saveTweets(tweets)
    return


if __name__ == '__main__':
    main()
