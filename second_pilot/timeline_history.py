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
games_col = db.gameCollection
stats = collection.find({"userId" : {"$nin": ["NNquJdDH2Hg2Nnhwp"]}})

stat_by_user = defaultdict(lambda: {"a": 0, "tl":{"a":0, "c": 0}, 'd': 0})

for stat in stats:
	user_id = stat["userId"]
	stat_by_user[user_id]["a"] += stat["amount"]
	stat_by_user[user_id]["d"] = items_col.count({"userId": user_id, "kindDifficulties.Timeline" : {"$gt":0.5}})
	
stat_by_user = {user_id: stat_by_user[user_id] for user_id in stat_by_user if stat_by_user[user_id]["d"] > 100}
stat_by_user = {user_id: stat_by_user[user_id] for user_id in stat_by_user if stat_by_user[user_id]["a"] > 3}

for user_id in stat_by_user:
	board_field = user_id + '_Board'
	user_games = games_col.find({board_field: {'$exists' : True}}).sort([("creationTime", -1)]).limit(3)
	cnt = 0
	for game in user_games:
		board = game[board_field]
		for tile in board["tiles"]:
			if tile["question1"]["kind"] == "Timeline":
				stat_by_user[user_id]["tl"]["a"] += 1
				if "correct" in tile["question1"] and tile["question1"]["correct"]:
					stat_by_user[user_id]["tl"]["c"] += 1

			if tile["question2"]["kind"] == "Timeline":
				stat_by_user[user_id]["tl"]["a"] += 1
				if "correct" in tile["question2"] and tile["question2"]["correct"]:
					stat_by_user[user_id]["tl"]["c"] += 1

			if tile["question3"]["kind"] == "Timeline":
				stat_by_user[user_id]["tl"]["a"] += 1
				if "correct" in tile["question3"] and tile["question3"]["correct"]:
					stat_by_user[user_id]["tl"]["c"] += 1

res_tl = [(stat_by_user[user_id]["tl"]["c"]/stat_by_user[user_id]["tl"]["a"]) * 100 for user_id in stat_by_user if stat_by_user[user_id]["tl"]["a"] > 0]
player_played = [stat_by_user[user_id]["a"] for user_id in stat_by_user if stat_by_user[user_id]["tl"]["a"] > 0]

plt.scatter(player_played, res_tl)

plt.title('Timeline questions games played/success rate scatter plot')

plt.xlabel('Games played')
plt.ylabel('Success rate (%)')

plt.show()