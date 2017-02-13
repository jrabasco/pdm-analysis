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

def analyse_question(question, counts):
	if "data" in question["answer"]:
		lat = question["answer"]["data"]["latitude"]
		longi = question["answer"]["data"]["longitude"]
		counts[(lat, longi)] += 1
	else:
		lat = question["answer"]["latitude"]
		longi = question["answer"]["longitude"]
		counts[(lat, longi)] += 1

def analyse_board(board, counts):
	for tile in board["tiles"]:
		if tile["question1"]["kind"] == "Geolocation":
			analyse_question(tile["question1"], counts)

		if tile["question2"]["kind"] == "Geolocation":
			analyse_question(tile["question2"], counts)
			
		if tile["question3"]["kind"] == "Geolocation":
			analyse_question(tile["question3"], counts)

def average_same(user_id, db):
	games_col = db.games
	counts = defaultdict(lambda: 0)
	user_games = games_col.find({})
	for game in user_games:
		if game['player1'] == user_id:
			analyse_board(game['player1Board'], counts)
		if game['player2'] == user_id:
			analyse_board(game['player2Board'], counts)

	values = list(counts.values())
	if len(values) > 0:
		return sum(values)/len(values)
	else:
		return 0

mongo_client = MongoClient('localhost', 27017)
db = mongo_client.pilot_2_stats
collection = db.statsCollection
items_col = db.itemsSummaries
stats = collection.find({"userId" : {"$nin": ["NNquJdDH2Hg2Nnhwp"]}})

stat_by_user = defaultdict(lambda: {"a": 0, "geo":{"a":0, "c": 0}, 'd': 0})

for stat in stats:
	user_id = stat["userId"]
	stat_by_user[user_id]["a"] += stat["amount"]
	stat_by_user[user_id]["geo"]["a"] += stat["questionsByType"]["geolocation"]["amount"]
	stat_by_user[user_id]["geo"]["c"] += stat["questionsByType"]["geolocation"]["correct"]

for user_id in stat_by_user:
	stat_by_user[user_id]["avg"] = average_same(user_id, db)

avgs = [stat_by_user[user_id]["avg"] for user_id in stat_by_user if stat_by_user[user_id]["geo"]["a"] > 0]
player_played = [stat_by_user[user_id]["a"] for user_id in stat_by_user if stat_by_user[user_id]["geo"]["a"] > 0]

plt.scatter(player_played, avgs)

plt.title('Geolocation questions games played/questions occurrences scatter plot')

plt.xlabel('Games played')
plt.ylabel('Questions occurrences')

plt.show()