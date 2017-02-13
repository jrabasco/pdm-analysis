from pymongo import MongoClient
import math
from matplotlib import pyplot as plt
import numpy as np
from dateutil import parser
from datetime import datetime, timezone

mongo_client = MongoClient('localhost', 27017)
db = mongo_client.pilot_2_stats
collection = db.statsCollection
stats = collection.find({"userId" : {"$ne": "NNquJdDH2Hg2Nnhwp"}})

mc_selected = 0
mc_correct = 0
mc_avoid = 0
tl_selected = 0
tl_correct = 0
tl_avoid = 0
geo_selected = 0
geo_correct = 0
geo_avoid = 0
ord_selected = 0
ord_correct = 0
ord_avoid = 0
questions = 0
cnt = 0

for stat in stats:
    cnt += 1
    mc_selected += stat["questionsByType"]["multipleChoice"]["amount"]
    mc_correct += stat["questionsByType"]["multipleChoice"]["correct"]
    mc_avoid += stat["questionsByType"]["multipleChoice"]["avoid"]
    tl_selected += stat["questionsByType"]["timeline"]["amount"]
    tl_correct += stat["questionsByType"]["timeline"]["correct"]
    tl_avoid += stat["questionsByType"]["timeline"]["avoid"]
    geo_selected += stat["questionsByType"]["geolocation"]["amount"]
    geo_correct += stat["questionsByType"]["geolocation"]["correct"]
    geo_avoid += stat["questionsByType"]["geolocation"]["avoid"]
    ord_selected += stat["questionsByType"]["order"]["amount"]
    ord_correct += stat["questionsByType"]["order"]["correct"]
    ord_avoid += stat["questionsByType"]["order"]["avoid"]
    questions += stat["questionsByType"]["multipleChoice"]["amount"]
    questions += stat["questionsByType"]["timeline"]["amount"]
    questions += stat["questionsByType"]["geolocation"]["amount"]
    questions += stat["questionsByType"]["order"]["amount"]


print(questions)
print(cnt)

N = 4
totals = (ord_selected, tl_selected, mc_selected, geo_selected)

ind = np.arange(N)  # the x locations for the groups
width = 0.25       # the width of the bars

fig, ax = plt.subplots()
rects1 = ax.bar(ind, totals, width, color='darkblue', align="center")

corrects = (ord_correct, tl_correct, mc_correct, geo_correct)
rects2 = ax.bar(ind + width + 0.05, corrects, width, color='lawngreen', align="center")

avoids = (ord_avoid, tl_avoid, mc_avoid, geo_avoid)
rects3 = ax.bar(ind + 2*width + 0.1, avoids, width, color='white', align="center")
print(totals)
print(corrects)
print(avoids)

# add some text for labels, title and axes ticks
ax.set_title('Answered, Correctly answered and Avoided Questions By Type')
ax.set_xticklabels(('Order', 'Timeline', 'Multiple Choice', 'Geolocation'))
ax.set_xticks(ind + 0.35)

ax.legend((rects1[0], rects2[0], rects3[0]), ('Total number of questions answered', 'Correctly answered questions', 'Avoided questions'))

plt.show()
