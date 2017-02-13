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
db = mongo_client.pilot_1_stats
games_col = db.games

counts = defaultdict(lambda: 0)

def analyse_question(question):
	global counts
	if "data" in question["answer"]:
		lat = question["answer"]["data"]["latitude"]
		longi = question["answer"]["data"]["longitude"]
		counts[(lat, longi)] += 1
	else:
		lat = question["answer"]["latitude"]
		longi = question["answer"]["longitude"]
		counts[(lat, longi)] += 1

def analyse_board(board):
	for tile in board["tiles"]:
		if tile["question1"]["kind"] == "Geolocation":
			analyse_question(tile["question1"])

		if tile["question2"]["kind"] == "Geolocation":
			analyse_question(tile["question2"])
			
		if tile["question3"]["kind"] == "Geolocation":
			analyse_question(tile["question3"])

user_games = games_col.find({})
for game in user_games:
	if game['player1'] != "658H6aC7EsqsKzGeW" and game['player1Board'] is not None:
		analyse_board(game['player1Board'])
	if game['player2'] != "658H6aC7EsqsKzGeW" and game['player2Board'] is not None:
		analyse_board(game['player2Board'])

values = list(counts.values())
freq_freqcount = sorted(set([(x, values.count(x)) for x in values]), key=lambda val: val[0])
freq = [val[0] for val in freq_freqcount]
freq_count = [val[1] for val in freq_freqcount]

print(freq_freqcount)
print("Average:", sum(values)/len(values))

plt.plot(freq, freq_count)
plt.xlabel('number of occurrences of a question')
plt.ylabel('amount of questions with that occurrence number')
plt.title('Geolocation questions occurrences')
plt.grid(True)
plt.show()