from pymongo import MongoClient
import math
from matplotlib import pyplot as plt
from dateutil import parser
from datetime import datetime, timezone

def unix_time_millis(dt):
    epoch = datetime.utcfromtimestamp(0).replace(tzinfo=timezone.utc)
    return int((dt  - epoch).total_seconds() * 1000)

mongo_client = MongoClient('localhost', 27017)
db = mongo_client.pilot_1_stats
collection = db.statsCollection
stats = collection.find({"userId" : {"$ne": "658H6aC7EsqsKzGeW"}})

questions = 0
games = 0

for stat in stats:
    games += stat["amount"]
    questions += stat["questionsByType"]["multipleChoice"]["amount"]
    questions += stat["questionsByType"]["timeline"]["amount"]
    questions += stat["questionsByType"]["geolocation"]["amount"]
    questions += stat["questionsByType"]["order"]["amount"]

print("Games:", games)
print("Games per user:", games/25)
print("Questions:", questions)