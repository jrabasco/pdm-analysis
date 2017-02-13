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

def subject_id(subject):
	identifier = ()
	if subject["type"] == "Page":
		identifier = ("Page", subject["name"], subject["pageId"])

	elif subject["type"] == "TextPost":
		identifier = ("TextPost", subject["text"])

	elif subject["type"] == "ImagePost":
		identifier = ("ImagePost", subject["text"], subject["thumbnailUrl"])

	elif subject["type"] == "VideoPost":
		identifier = ("ImagePost", subject["text"], subject["thumbnailUrl"], subject["url"])

	elif subject["type"] == "LinkPost":
		identifier = ("LinkPost", subject["text"], subject["thumbnailUrl"], subject["url"])
	return identifier


def analyse_question(question, counts):
	subject = question["subject"]
	identifier = subject_id(subject)
	counts[identifier] += 1

def analyse_board(board, counts):
	for tile in board["tiles"]:
		if tile["question1"]["kind"] == "Timeline":
			analyse_question(tile["question1"], counts)

		if tile["question2"]["kind"] == "Timeline":
			analyse_question(tile["question2"], counts)
			
		if tile["question3"]["kind"] == "Timeline":
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

stat_by_user = defaultdict(lambda: {"a": 0, "tl":{"a":0, "c": 0}, 'd': 0})

for stat in stats:
	user_id = stat["userId"]
	stat_by_user[user_id]["a"] += stat["amount"]
	stat_by_user[user_id]["tl"]["a"] += stat["questionsByType"]["timeline"]["amount"]
	stat_by_user[user_id]["tl"]["c"] += stat["questionsByType"]["timeline"]["correct"]

for user_id in stat_by_user:
	stat_by_user[user_id]["avg"] = average_same(user_id, db)

avgs = [stat_by_user[user_id]["avg"] for user_id in stat_by_user if stat_by_user[user_id]["tl"]["a"] > 0]
player_played = [stat_by_user[user_id]["a"] for user_id in stat_by_user if stat_by_user[user_id]["tl"]["a"] > 0]

plt.scatter(player_played, avgs)

plt.title('Timeline questions games played/questions occurrences scatter plot')

plt.xlabel('Games played')
plt.ylabel('Questions occurrences')

plt.show()