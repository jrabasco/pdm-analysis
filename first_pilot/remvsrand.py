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
collection = db.statsCollection
stats = collection.find({"userId" : {"$ne": "658H6aC7EsqsKzGeW"}})

stat_by_user = defaultdict(lambda: {"mc":{"a":0, "c": 0}, "tl":{"a":0, "c": 0}, "geo":{"a":0, "c": 0},"ord":{"a":0, "c": 0}})

for stat in stats:
	user_id = stat["userId"]
	stat_by_user[user_id]["mc"]["a"] += stat["questionsByType"]["multipleChoice"]["amount"]
	stat_by_user[user_id]["mc"]["c"] += stat["questionsByType"]["multipleChoice"]["correct"]

	stat_by_user[user_id]["tl"]["a"] += stat["questionsByType"]["timeline"]["amount"]
	stat_by_user[user_id]["tl"]["c"] += stat["questionsByType"]["timeline"]["correct"]
    
	stat_by_user[user_id]["geo"]["a"] += stat["questionsByType"]["geolocation"]["amount"]
	stat_by_user[user_id]["geo"]["c"] += stat["questionsByType"]["geolocation"]["correct"]
    
	stat_by_user[user_id]["ord"]["a"] += stat["questionsByType"]["order"]["amount"]
	stat_by_user[user_id]["ord"]["c"] += stat["questionsByType"]["order"]["correct"]

res_mc = [(stat_by_user[user_id]["mc"]["c"]/stat_by_user[user_id]["mc"]["a"]) * 100 for user_id in stat_by_user if stat_by_user[user_id]["mc"]["a"] > 0]
res_tl = [(stat_by_user[user_id]["tl"]["c"]/stat_by_user[user_id]["tl"]["a"]) * 100 for user_id in stat_by_user if stat_by_user[user_id]["tl"]["a"] > 0]
res_geo = [(stat_by_user[user_id]["geo"]["c"]/stat_by_user[user_id]["geo"]["a"]) * 100 for user_id in stat_by_user if stat_by_user[user_id]["geo"]["a"] > 0]
res_ord = [(stat_by_user[user_id]["ord"]["c"]/stat_by_user[user_id]["ord"]["a"]) * 100 for user_id in stat_by_user if stat_by_user[user_id]["ord"]["a"] > 0]

ord_correct = np.mean(res_ord)
ord_std = np.std(res_ord)

tl_correct = np.mean(res_tl)
tl_std = np.std(res_tl)

mc_correct = np.mean(res_mc)
mc_std = np.std(res_mc)

geo_correct = np.mean(res_geo)
geo_std = np.std(res_geo)

N = 4
corrects = (ord_correct, tl_correct, mc_correct, geo_correct)
corrects_std = (ord_std, tl_std, mc_std, geo_std)

ind = np.arange(N)  # the x locations for the groups
width = 0.35       # the width of the bars

fig, ax = plt.subplots()
rects1 = ax.bar(ind, corrects, width, color='lawngreen', align="center", yerr=corrects_std, error_kw={'ecolor':'red', 'elinewidth':2, 'capthick': 2})

expected = (16.66666, 33.333333, 25, 0)
rects2 = ax.bar(ind, expected, width, color='darkblue', align="center")

print(corrects)

# add some text for labels, title and axes ticks
ax.set_title('Percentages Correctly Answered')
ax.set_xticklabels(('Order', 'Timeline', 'Multiple Choice', 'Geolocation'))
ax.set_xticks(ind)

ax.legend((rects1[0], rects2[0]), ('%correct', '%correct at random'), loc='upper left')
ax.set_xlabel('Question Type')
ax.set_ylabel('Percentage Correct')

plt.show()