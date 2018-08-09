#!/usr/bin/ python
# -*- coding:utf-8 -*-

import os,sys
import nltk,math,re,pprint
import json

from pymongo import MongoClient

mongo_db = MongoClient('localhost', 27017).get_database('test')
df = get_data_from_mongo(mongo_db)

def get_data_from_mongo(db):
    tuples = []
    for doc in db.get_collection('news').find():
        tuples.append((doc['domain'], str(doc['_id']), doc['title'], doc['content'], doc['publish_time'], doc['website'],doc['keywords']))
        print tuples
        return tuples

