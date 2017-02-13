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
items_col = db.itemsSummaries
stats = collection.find({"userId" : {"$nin": ["NNquJdDH2Hg2Nnhwp"]}})

stat_by_user = defaultdict(lambda: {"a": 0, "tl":{"a":0, "c": 0}, 'd': 0})

for stat in stats:
	user_id = stat["userId"]
	stat_by_user[user_id]["a"] += stat["amount"]
	stat_by_user[user_id]["tl"]["a"] += stat["questionsByType"]["timeline"]["amount"]
	stat_by_user[user_id]["tl"]["c"] += stat["questionsByType"]["timeline"]["correct"]
	#stat_by_user[user_id]["d"] = items_col.count({"userId": user_id, "kindDifficulties.Timeline" : {"$gt":0.5}})
	
#stat_by_user = {user_id: stat_by_user[user_id] for user_id in stat_by_user if stat_by_user[user_id]["d"] > 200}
res_tl = [(stat_by_user[user_id]["tl"]["c"]/stat_by_user[user_id]["tl"]["a"]) * 100 for user_id in stat_by_user if stat_by_user[user_id]["tl"]["a"] > 0]
player_played = [stat_by_user[user_id]["a"] for user_id in stat_by_user if stat_by_user[user_id]["tl"]["a"] > 0]

plt.scatter(player_played, res_tl)

plt.title('Timeline questions games played/success rate scatter plot')

plt.xlabel('Games played')
plt.ylabel('Success rate (%)')

plt.show()