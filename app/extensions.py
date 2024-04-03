from flask_pymongo import pymongo

# Setup MongoDB here
client = pymongo.MongoClient("mongodb://localhost:27017/")

db = client['WebHook']
collection = db['webhook']