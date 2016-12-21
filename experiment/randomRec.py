# randomly recommend 5 apps and compute rewards

import numpy as np
import match_app_v2 as match_app

# read in file
tmp = []
with open("../DataFile/session.txt", "r") as f:
    for line in f:
        line = line.strip().rstrip(',').split(',')
        line = list(map(float, line))
        tmp.append(line)
    f.close()
data = np.asarray(tmp)

tmp = []
with open("../DataFile/app_feature.txt", "r") as f:
    for line in f:
        line = line.strip().rstrip(',').split(',')
        line= list(map(float, line))
        tmp.append(line)
    f.close()
app = np.asarray(tmp)

# initialization
session_n = int(max(data[:, 0]))
pool_size = app.shape[0]
ratio = 0.5
K = 5
click_n = 0
cnt = 0
click_n = 0

idx = np.random.permutation(session_n) +1
ts_idx = idx[int(round(session_n * ratio)):]
# print ts_idx


# randomly pick K apps
def random_app(number=K):
    app_idx = np.random.permutation(pool_size)+1
    rec = app_idx[:number]
    return rec

# randomly get session
for i in range(ts_idx.shape[0]):
    record = data[np.where(data[:, 0] == ts_idx[i])]
    action = random_app()
    reward = match_app.match(record, action)
    if reward is not None:
        for j in reward:
            if reward[j] == 1 or reward[j] == 0:
                cnt += 1
                click_n += reward[j]
    else:
        continue

result = float(click_n) / cnt
print "the reward of random recommend is: %s" % result



