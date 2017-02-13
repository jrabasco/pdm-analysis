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

stat_by_user = defaultdict(lambda: {"mc":{"a":0, "t": 0}, "tl":{"a":0, "t": 0}, "geo":{"a":0, "t": 0},"ord":{"a":0, "t": 0}})

for stat in stats:
	user_id = stat["userId"]
	stat_by_user[user_id]["mc"]["a"] += stat["questionsByType"]["multipleChoice"]["amount"]
	stat_by_user[user_id]["mc"]["t"] += stat["questionsByType"]["multipleChoice"]["timeSpent"]/1000

	stat_by_user[user_id]["tl"]["a"] += stat["questionsByType"]["timeline"]["amount"]
	stat_by_user[user_id]["tl"]["t"] += stat["questionsByType"]["timeline"]["timeSpent"]/1000
    
	stat_by_user[user_id]["geo"]["a"] += stat["questionsByType"]["geolocation"]["amount"]
	stat_by_user[user_id]["geo"]["t"] += stat["questionsByType"]["geolocation"]["timeSpent"]/1000
    
	stat_by_user[user_id]["ord"]["a"] += stat["questionsByType"]["order"]["amount"]
	stat_by_user[user_id]["ord"]["t"] += stat["questionsByType"]["order"]["timeSpent"]/1000

res_mc = [(stat_by_user[user_id]["mc"]["t"]/stat_by_user[user_id]["mc"]["a"]) for user_id in stat_by_user if stat_by_user[user_id]["mc"]["a"] > 0]
res_tl = [(stat_by_user[user_id]["tl"]["t"]/stat_by_user[user_id]["tl"]["a"]) for user_id in stat_by_user if stat_by_user[user_id]["tl"]["a"] > 0]
res_geo = [(stat_by_user[user_id]["geo"]["t"]/stat_by_user[user_id]["geo"]["a"]) for user_id in stat_by_user if stat_by_user[user_id]["geo"]["a"] > 0]
res_ord = [(stat_by_user[user_id]["ord"]["t"]/stat_by_user[user_id]["ord"]["a"]) for user_id in stat_by_user if stat_by_user[user_id]["ord"]["a"] > 0]

data = [res_ord, res_tl, res_mc, res_geo]

fig, ax1 = plt.subplots(figsize=(10, 6))
fig.canvas.set_window_title('A Boxplot Example')
plt.subplots_adjust(left=0.075, right=0.95, top=0.9, bottom=0.25)

bp = plt.boxplot(data, notch=0, sym='+', vert=1, whis=1.5)
plt.setp(bp['boxes'], color='black')
plt.setp(bp['whiskers'], color='black')
plt.setp(bp['fliers'], color='red', marker='+')

# Add a horizontal grid to the plot, but make it very light in color
# so we can use it for reading data values but not be distracting
ax1.yaxis.grid(True, linestyle='-', which='major', color='lightgrey',
               alpha=0.5)

# Hide these grid behind plot objects
ax1.set_axisbelow(True)
ax1.set_title('Box Plot Of Time Spent By Type')
ax1.set_xlabel('Question Type')
ax1.set_ylabel('Time [s]')

# Set the axes ranges and axes labels
ax1.set_xlim(0.5, 4 + 0.5)
top = 28
bottom = 2
ax1.set_ylim(bottom, top)
xtickNames = plt.setp(ax1, xticklabels=['Order', 'Timeline', 'Multiple Choice', 'Geolocation'])
plt.setp(xtickNames, fontsize=8)

pos = np.arange(4) + 1
weights = ['bold', 'semibold']
for tick, label in zip(range(4), ax1.get_xticklabels()):
    k = tick % 2
    ax1.text(pos[tick], top - (top*0.05), '',
             horizontalalignment='center', size='x-small', weight=weights[k])

plt.show()