from pymongo import MongoClient
import math
from matplotlib import pyplot as plt
import numpy as np
from dateutil import parser
from datetime import datetime, timezone
from collections import defaultdict
from scipy import stats as st

def unix_time_millis(dt):
    epoch = datetime.utcfromtimestamp(0).replace(tzinfo=timezone.utc)
    return int((dt  - epoch).total_seconds() * 1000)

mongo_client = MongoClient('localhost', 27017)

db1 = mongo_client.pilot_1_stats
collection1 = db1.statsCollection
stats1 = collection1.find({"userId" : {"$ne": "658H6aC7EsqsKzGeW"}})

stat_by_user1 = defaultdict(lambda: {"mc":{"a":0, "c": 0}, "tl":{"a":0, "c": 0}, "geo":{"a":0, "c": 0},"ord":{"a":0, "c": 0}})

for stat in stats1:
	user_id = stat["userId"]
	stat_by_user1[user_id]["mc"]["a"] += stat["questionsByType"]["multipleChoice"]["amount"]
	stat_by_user1[user_id]["mc"]["c"] += stat["questionsByType"]["multipleChoice"]["correct"]

	stat_by_user1[user_id]["tl"]["a"] += stat["questionsByType"]["timeline"]["amount"]
	stat_by_user1[user_id]["tl"]["c"] += stat["questionsByType"]["timeline"]["correct"]
    
	stat_by_user1[user_id]["geo"]["a"] += stat["questionsByType"]["geolocation"]["amount"]
	stat_by_user1[user_id]["geo"]["c"] += stat["questionsByType"]["geolocation"]["correct"]
    
	stat_by_user1[user_id]["ord"]["a"] += stat["questionsByType"]["order"]["amount"]
	stat_by_user1[user_id]["ord"]["c"] += stat["questionsByType"]["order"]["correct"]

res_mc1 = [(stat_by_user1[user_id]["mc"]["c"]/stat_by_user1[user_id]["mc"]["a"]) * 100 for user_id in stat_by_user1 if stat_by_user1[user_id]["mc"]["a"] > 0]
res_tl1 = [(stat_by_user1[user_id]["tl"]["c"]/stat_by_user1[user_id]["tl"]["a"]) * 100 for user_id in stat_by_user1 if stat_by_user1[user_id]["tl"]["a"] > 0]
res_geo1 = [(stat_by_user1[user_id]["geo"]["c"]/stat_by_user1[user_id]["geo"]["a"]) * 100 for user_id in stat_by_user1 if stat_by_user1[user_id]["geo"]["a"] > 0]
res_ord1 = [(stat_by_user1[user_id]["ord"]["c"]/stat_by_user1[user_id]["ord"]["a"]) * 100 for user_id in stat_by_user1 if stat_by_user1[user_id]["ord"]["a"] > 0]

db2 = mongo_client.pilot_2_stats
collection2 = db2.statsCollection
stats2 = collection2.find({"userId" : {"$ne": "NNquJdDH2Hg2Nnhwp"}})

stat_by_user2 = defaultdict(lambda: {"mc":{"a":0, "c": 0}, "tl":{"a":0, "c": 0}, "geo":{"a":0, "c": 0},"ord":{"a":0, "c": 0}})

for stat in stats2:
	user_id = stat["userId"]
	stat_by_user2[user_id]["mc"]["a"] += stat["questionsByType"]["multipleChoice"]["amount"]
	stat_by_user2[user_id]["mc"]["c"] += stat["questionsByType"]["multipleChoice"]["correct"]

	stat_by_user2[user_id]["tl"]["a"] += stat["questionsByType"]["timeline"]["amount"]
	stat_by_user2[user_id]["tl"]["c"] += stat["questionsByType"]["timeline"]["correct"]
    
	stat_by_user2[user_id]["geo"]["a"] += stat["questionsByType"]["geolocation"]["amount"]
	stat_by_user2[user_id]["geo"]["c"] += stat["questionsByType"]["geolocation"]["correct"]
    
start = datetime(2017, 1, 18, 0, 0, 0)
stats22 = collection2.find({"userId" : {"$nin": ["NNquJdDH2Hg2Nnhwp"]}, "date":{"$gte": start}})
for stat in stats22:
	user_id = stat["userId"]
	stat_by_user2[user_id]["ord"]["a"] += stat["questionsByType"]["order"]["amount"]
	stat_by_user2[user_id]["ord"]["c"] += stat["questionsByType"]["order"]["correct"]

res_mc2 = [(stat_by_user2[user_id]["mc"]["c"]/stat_by_user2[user_id]["mc"]["a"]) * 100 for user_id in stat_by_user2 if stat_by_user2[user_id]["mc"]["a"] > 0]
res_tl2 = [(stat_by_user2[user_id]["tl"]["c"]/stat_by_user2[user_id]["tl"]["a"]) * 100 for user_id in stat_by_user2 if stat_by_user2[user_id]["tl"]["a"] > 0]
res_geo2 = [(stat_by_user2[user_id]["geo"]["c"]/stat_by_user2[user_id]["geo"]["a"]) * 100 for user_id in stat_by_user2 if stat_by_user2[user_id]["geo"]["a"] > 0]
res_ord2 = [(stat_by_user2[user_id]["ord"]["c"]/stat_by_user2[user_id]["ord"]["a"]) * 100 for user_id in stat_by_user2 if stat_by_user2[user_id]["ord"]["a"] > 0]

print(st.ttest_ind(res_ord1, res_ord2))
print(st.ttest_ind(res_tl1, res_tl2))
print(st.ttest_ind(res_mc1, res_mc2))
print(st.ttest_ind(res_geo1, res_geo2))