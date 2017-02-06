# randomly recommend 5 apps and compute rewards

import numpy as np
import match_app
import time
from time import localtime, strftime

def readSess(i):
    tmp = []
    filename = '../session_bootstrap' + str(i+1) + '.txt'
    with open(filename, "r") as f:
        for line in f:
            line = line.strip().rstrip(',').split(',')
            line = list(map(float, line))
            tmp.append(line)
        f.close()
    data = np.asarray(tmp)
    return data
    
def readDict(i):
    tmp = []
    dictname = '../sid_dict' + str(i+1) + '.txt'
    with open(dictname, "r") as f:
        for line in f:
            line = line.strip().split(',')
            for i in range(0,int(line[1])):
                tmp.append(line[0])
        f.close()
    data = np.asarray(tmp)
    return data
    
# randomly pick K apps
def random_app(number=K):
    app_idx = np.random.permutation(pool_size)+1
    rec = app_idx[:number]
    return rec

tmp = []
with open("../app_feature.txt", "r") as f:
    for line in f:
        line = line.strip().rstrip(',').split(',')
        line= list(map(float, line))
        tmp.append(line)
    f.close()
app = np.asarray(tmp)

B=3
reward_acc=0
cnt_acc = 0
cur_time = strftime("%Y%m%d_",localtime())
logFileName = '../LogFile/random_BT_' + cur_time + '.txt'
logFile = open(logFileName, 'w')
print >>logFile, '\n\n'
print >>logFile, '='*50
print >>logFile, '\n\n'

for t in range(0,B):
    print "Round " + str(t+1) + " starts!"
    data = readSess(t)
    sids = readDict(t)
    # initialization
    session_n = sids.shape[0]
    pool_size = app.shape[0]
    ratio = 0.7
    K = 5
    click_n = 0
    cnt = 0
    click_n = 0

    tr_idx = sids[:int(round(session_n * ratio))]
    ts_idx = sids[int(round(session_n * ratio)):]
    
    expl = np.zeros(pool_size)
    # randomly get session
    for i in range(ts_idx.shape[0]):
        record = data[np.where(data[:, 0] == float(ts_idx[i]))]
        action = random_app(K)
        reward = match_app.match(record, action)
        if reward is not None:
            for j in reward:
                if reward[j] == 1 or reward[j] == 0:
                    cnt += 1
                    click_n += reward[j]
        else:
            continue

    result = float(click_n) / cnt
    reward_acc += result
    cnt_acc += cnt
    print >>logFile, "the cnt is: %s" % cnt
    print >>logFile, "the reward of random recommend is: %s" % result

cnt_avg = cnt_acc/B
print >>logFile, "the avg_cnt is: %s" % cnt_avg
reward_avg = reward_acc/B
print >>logFile, "the avg_reward of random recommend is: %s" % reward_avg
