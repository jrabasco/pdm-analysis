from pymongo import MongoClient
import math
from matplotlib import pyplot as plt
from dateutil import parser
from datetime import datetime, timezone

def unix_time_millis(dt):
    epoch = datetime.utcfromtimestamp(0).replace(tzinfo=timezone.utc)
    return int((dt  - epoch).total_seconds() * 1000)

mongo_client = MongoClient('localhost', 27017)
db = mongo_client.pilot_2_stats
collection = db.statsCollection
stats = collection.find({"userId" : {"$ne": "NNquJdDH2Hg2Nnhwpa"}})

questions = 0
games = 155
users = []

for stat in stats:
    users.append(stat["userId"])
    questions += stat["questionsByType"]["multipleChoice"]["amount"]
    questions += stat["questionsByType"]["timeline"]["amount"]
    questions += stat["questionsByType"]["geolocation"]["amount"]
    questions += stat["questionsByType"]["order"]["amount"]
print(len(users))
users = set(users)
print("Users:", len(users))
print("Games:", games)
print("Games per user:", games)
print("Questions:", questions)