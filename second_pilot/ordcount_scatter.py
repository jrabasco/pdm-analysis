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

	elif subject["type"] == "Comment":
		identifier = ("Comment", subject["comment"], subject_id(subject["post"]))
	else:
		print(subject["type"])

	return identifier

def choice_id(choice):
	return (choice["text"], choice["fbId"])

def choices_id(choices):
	return tuple(sorted([choice_id(choice) for choice in choices], key=lambda val: val[1]))


def analyse_question(question, counts):
	
	if question["type"] == "ORDPostReactionsNumber":
		identifier = subject_id(question["subject"])
	else:
		sorted_items = sorted(question["items"], key=lambda val: val["subject"]["pageId"])
		identifier = tuple([subject_id(item["subject"]) for item in sorted_items])

	counts[identifier] += 1

def analyse_board(board, counts):
	for tile in board["tiles"]:
		if tile["question1"]["kind"] == "Order":
			analyse_question(tile["question1"], counts)

		if tile["question2"]["kind"] == "Order":
			analyse_question(tile["question2"], counts)
			
		if tile["question3"]["kind"] == "Order":
			analyse_question(tile["question3"], counts)

def average_same(user_id, db):
	games_col = db.games
	counts = defaultdict(lambda: 0)
	start = datetime(2017, 1, 18, 0, 0, 0)
	user_games = games_col.find({"creationTime" : {"$gte": start}})
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

for user_id in stat_by_user:
	stat_by_user[user_id]["avg"] = average_same(user_id, db)

avgs = [stat_by_user[user_id]["avg"] for user_id in stat_by_user if stat_by_user[user_id]["ord"]["a"] > 0]
player_played = [stat_by_user[user_id]["a"] for user_id in stat_by_user if stat_by_user[user_id]["ord"]["a"] > 0]

plt.scatter(player_played, avgs)

plt.title('Order questions games played/questions occurrences scatter plot')

plt.xlabel('Games played')
plt.ylabel('Questions occurrences')

plt.show()