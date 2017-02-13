from pymongo import MongoClient
import math
from matplotlib import pyplot as plt
import numpy as np
from dateutil import parser
from datetime import datetime, timezone
from collections import defaultdict

mongo_client = MongoClient('localhost', 27017)
db = mongo_client.pilot_1_stats
games_col = db.games

counts = defaultdict(lambda: 0)

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
		identifier = ("Comment", subject["comment"])
	else:
		print(subject["type"])

	return identifier

def choice_id(choice):
	return (choice["text"], choice["fbId"])

def choices_id(choices):
	return tuple(sorted([choice_id(choice) for choice in choices], key=lambda val: val[1]))


def analyse_question(question):
	global counts
	
	if question["type"] == "MCWhichPageDidYouLike":
		identifier = choices_id(question["choices"])
	else:
		subject = question["subject"]
		subject_identifier = subject_id(subject)
		answer = int(question["answer"])
		answer_id = choice_id(question["choices"][answer])
		identifier = (subject_identifier, answer_id)

	counts[identifier] += 1

def analyse_board(board):
	for tile in board["tiles"]:
		if tile["question1"]["kind"] == "MultipleChoice":
			analyse_question(tile["question1"])

		if tile["question2"]["kind"] == "MultipleChoice":
			analyse_question(tile["question2"])
			
		if tile["question3"]["kind"] == "MultipleChoice":
			analyse_question(tile["question3"])

user_games = games_col.find({})
for game in user_games:
	if game['player1'] != "658H6aC7EsqsKzGeW" and game['player1Board'] is not None:
		analyse_board(game['player1Board'])
	if game['player2'] != "658H6aC7EsqsKzGeW" and game['player1Board'] is not None:
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
plt.title('Multiple choice questions occurrences')
plt.grid(True)
plt.show()