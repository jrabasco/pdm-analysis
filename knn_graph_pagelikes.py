from pymongo import MongoClient
import math
from matplotlib import pyplot as plt

mongo_client = MongoClient('localhost', 27017)
db = mongo_client.pilot_gc
collection = db.fbPages
pages = collection.find({})

like_numbers = [page["likesNumber"] for page in pages]
sorted_likes = sorted(like_numbers)
sorted_log_likes = [math.log(number) for number in sorted_likes]

distances = []

for i, x in enumerate(sorted_log_likes):
    if i == 0:
        distances.append(sorted_log_likes[2] - x)
    elif i == 1:
        distances.append(max(x - sorted_log_likes[0], sorted_log_likes[3] -x))
    elif i == len(sorted_log_likes) - 1:
        distances.append(x - sorted_log_likes[-3])
    elif i == len(sorted_log_likes) - 2:
        distances.append(max(sorted_log_likes[-1] - x, x - sorted_log_likes[i-2]))
    else:
        distances.append(max(x - sorted_log_likes[i-2], sorted_log_likes[i+2] - x))

sorted_distances = sorted(distances)
x_space = range(len(sorted_distances))

plt.plot(x_space, sorted_distances)
for xy in zip(x_space, sorted_distances):
    if xy[0] == 129:
        nxy = (xy[0], int(100000*xy[1])/100000)
        plt.annotate('(%s, %s)' % nxy, xy=xy, textcoords='data') # <--
plt.xlabel("Points")
plt.ylabel("Distance (logarithm of likes number)")
plt.title("Page likes number 3-distances graph")
plt.savefig("page_likes_number_knn.pdf")
plt.show()
