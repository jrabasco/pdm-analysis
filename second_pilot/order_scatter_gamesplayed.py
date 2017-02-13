from pymongo import MongoClient
import math
from matplotlib import pyplot as plt
import numpy as np
from dateutil import parser
from datetime import datetime, timezone
from collections import defaultdict

def unix_time_millis(dt):
    epoch = datetime.utcfromtimestamp(0).replace(tzinfo=timezone.utc)
    return int((dt  - epoch).total_seconds() * 1000)

mongo_client = MongoClient('localhost', 27017)
db = mongo_client.pilot_2_stats
collection = db.statsCollection
stats = collection.find({"userId" : {"$nin": ["NNquJdDH2Hg2Nnhwp"]}})

stat_by_user = defaultdict(lambda: {"a": 0, "ord":{"a":0, "c": 0}})

for stat in stats:
	user_id = stat["userId"]
	stat_by_user[user_id]["a"] += stat["amount"]
	

start = datetime(2017, 1, 18, 0, 0, 0)
stats2 = collection.find({"userId" : {"$nin": ["NNquJdDH2Hg2Nnhwp"]}, "date":{"$gte": start}})
for stat in stats2:
	user_id = stat["userId"]
	stat_by_user[user_id]["ord"]["a"] += stat["questionsByType"]["order"]["amount"]
	stat_by_user[user_id]["ord"]["c"] += stat["questionsByType"]["order"]["correct"]

res_ord = [(stat_by_user[user_id]["ord"]["c"]/stat_by_user[user_id]["ord"]["a"]) * 100 for user_id in stat_by_user if stat_by_user[user_id]["ord"]["a"] > 0]
player_played = [stat_by_user[user_id]["a"] for user_id in stat_by_user if stat_by_user[user_id]["ord"]["a"] > 0]

plt.scatter(player_played, res_ord)

plt.title('Order questions games played/success rate scatter plot')

plt.xlabel('Games played')
plt.ylabel('Success rate (%)')

plt.show()