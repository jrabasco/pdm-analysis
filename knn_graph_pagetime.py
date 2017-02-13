from pymongo import MongoClient
import math
from matplotlib import pyplot as plt
from dateutil import parser
from datetime import datetime, timezone

def unix_time_millis(dt):
    epoch = datetime.utcfromtimestamp(0).replace(tzinfo=timezone.utc)
    dtutc = dt.replace(tzinfo=timezone.utc)
    return int((dtutc  - epoch).total_seconds() * 1000)

mongo_client = MongoClient('localhost', 27017)
db = mongo_client.pilot_gc
collection = db.fbPageLikes
pages = collection.find({"userId" : "1300814849933171"})

pages_dates = [page["likeTime"] for page in pages]
pages_timestamps = [unix_time_millis(dt) for dt in pages_dates]

sorted_ts = sorted(pages_timestamps)

distances = []

for i, x in enumerate(sorted_ts):
    if i == 0:
        distances.append(sorted_ts[2] - x)
    elif i == 1:
        distances.append(max(x - sorted_ts[0], sorted_ts[3] -x))
    elif i == len(sorted_ts) - 1:
        distances.append(x - sorted_ts[-3])
    elif i == len(sorted_ts) - 2:
        distances.append(max(sorted_ts[-1] - x, x - sorted_ts[i-2]))
    else:
        distances.append(max(x - sorted_ts[i-2], sorted_ts[i+2] - x))

sorted_distances = sorted(distances)
x_space = range(len(sorted_distances))

plt.plot(x_space, sorted_distances)

for xy in zip(x_space, sorted_distances):
    if xy[0] == 122:
        nxy = (xy[0], int(100000*xy[1])/100000)
        plt.annotate('(%s, %s)' % nxy, xy=xy, textcoords='data') # <--
plt.xlabel("Points")
plt.ylabel("Distance (x10^9 milliseconds)")
plt.title("Page like time 3-distances graph")
plt.savefig("page_like_time_knn.pdf")
plt.show()
