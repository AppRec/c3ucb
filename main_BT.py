import numpy as np
import match_app
import utils
import time

#read in file
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

tmp=[]
with open("../user_feature.txt", "r") as f:
    for line in f:
        line = line.strip().rstrip(',').split(',')
        line = list(map(float, line))
        tmp.append(line)
    f.close()
user = np.asarray(tmp)

tmp=[]
with open("../app_feature.txt", "r") as f:
    for line in f:
        line = line.strip().rstrip(',').split(',')
        line= list(map(float, line))
        tmp.append(line)
    f.close()
app = np.asarray(tmp)

#initialization
B=3
reward_acc=0
for i in range(0,B):
    print "Round " + str(i+1) + " starts!"
    data = readSess(i)
    sids = readDict(i)
    start = time.clock()
    pool_size = app.shape[0]
    user_row_n = user.shape[1]
    app_row_n = app.shape[1]
    d = int((user_row_n-1)*(app_row_n-1))
    session_n = sids.shape[0]
    train_ratio = 0.7
    gamma = 1
    lamb = 0.5
    theta = np.zeros(d)
    beta = 1
    delta = 0.9
    V = lamb * np.eye(d)
    X = np.zeros((1, d), dtype = np.float)
    Y = np.zeros(1)
    x_feature = np.zeros((pool_size,d), dtype = np.float)
    UCB = np.zeros(pool_size, dtype = np.float)
    #session = np.zeros(session_n, dtype = np.float)
    K = 5
    click_n = 0

    #idx = np.random.permutation(session_n) +1
    sids = np.random.permutation(sids)
    tr_idx = sids[:int(round(session_n * train_ratio))]
    ts_idx = sids[int(round(session_n * train_ratio)):]

    #train
    app = app[:,1:]
    expl = np.zeros(pool_size)
    for i in range(tr_idx.shape[0]):
        record = np.zeros(1)
        u = np.zeros(1)
        try:
            record = data[np.where(data[:, 0] == tr_idx[i])]
            u = user[np.where(user[:, 0] == record[0, 0])][0,1:]
        except IndexError:
            continue
        else:
            for a in range(pool_size):
                x_feature[a] = np.outer(u, app[a, :]).reshape(1, d)
                x_feature[a] = np.divide(x_feature[a], np.linalg.norm(x_feature[a]))
                UCB[a] = utils.getUCB(theta, x_feature[a], beta, V)
                #print "this is app "+str(a)+" UCB is " + str(UCB[a])
            action = UCB.argsort()[-K:][::-1]
            for ii in range(K):
                if expl[action[ii]] == 0:
                    expl[action[ii]] = 1
            # print expl
            reward = match_app.match(record, action+1)
            idx=[]
            val=[]
            if reward is not None:
                for j in reward:
                    if reward[j]==1 or reward[j]==0:
                        idx.append(j)
                        val.append(reward[j])
                idx = np.asarray(idx)
                val = np.asarray(val)
                x_t = x_feature[idx-1,:]
                w = np.array(val.reshape(x_t.shape[0],1))
                print w
                [V, X, Y, theta, beta] = utils.update_stat(V, x_t, X, Y, w, lamb, delta)

            else:
                continue

    #test
    cnt = 0
    result = [0]
    for i in range(ts_idx.shape[0]):
        record = np.zeros(1)
        u = np.zeros(1)
        try:
            record = data[np.where(data[:, 0] == ts_idx[i])]
            u = user[np.where(user[:, 0] == record[0, 0])][0,1:]
        except IndexError:
            continue
        else:
            for a in range(pool_size):
                x_feature[a] = np.outer(u, app[a, :]).reshape(1, d)
                x_feature[a] = np.divide(x_feature[a], np.linalg.norm(x_feature[a]))
                UCB[a] = utils.getUCB(theta, x_feature[a], beta, V)   
                #print "this is app "+str(a)+" UCB is " + str(UCB[a])
            action = UCB.argsort()[-K:][::-1]
            for ii in range(K):
                if expl[action[ii]]==0:
                    expl[action[ii]]=1
            print expl
            reward = match_app.match(record, action+1)
            idx=[]
            val=[]
            if reward is not None:
                for j in reward:
                    if reward[j]==1 or reward[j]==0:
                        cnt = cnt+1
                        idx.append(j)
                        val.append(reward[j])
                idx = np.asarray(idx)
                val = np.asarray(val)
                x_t = x_feature[idx-1,:]
                w = np.array(val.reshape(x_t.shape[0],1))
                print w
                [V, X, Y, theta, beta] = utils.update_stat(V, x_t, X, Y, w, lamb, delta)
                click_n = click_n + utils.get_reward(w)
                result.append((float(click_n)/cnt))
                print result
            else:
                continue
                
    print "the reward is: %s" % result
    print "cnt is: %s" % cnt
    expl_n = sum(expl)
    expl_n_rate = float(expl_n/pool_size)
    print "expl_n is %s" % str(expl_n)
    print "expl_rate is %s" % str(expl_n_rate)
    reward_acc += result

reward_avg = reward_acc/B
print "the average reward is: %s" % reward_avg