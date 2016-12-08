import numpy as np
import match_app
import utils

#read in file
tmp = []
with open("session.txt", "r") as f:
    for line in f:
        line = line.strip().rstrip(',').split(',')
        # py2
        # data = map(float,data)
        # py3
        #print(line)
        line = list(map(float, line))
        tmp.append(line)
    f.close()
data = np.asarray(tmp)
tmp=[]

with open("user_feature.txt", "r") as f:
    for line in f:
        line = line.strip().rstrip(',').split(',')
        # py2
        # user = map(float,user)
        # py3
        line = list(map(float, line))
        tmp.append(line)
    f.close()
user = np.asarray(tmp)
tmp=[]

with open("extracted_app_feature.txt", "r") as f:
    for line in f:
        line = line.strip().rstrip(',').split(',')
        # py2
        # user = map(float,user)
        # py3
        line= list(map(float, line))
        tmp.append(line)
    f.close()
app = np.asarray(tmp)
    
#initialization
print app.shape
pool_size = app.shape[0]
user_row_n = user.shape[1]
app_row_n = app.shape[1]
d = int((user_row_n-1)*(app_row_n-1))
session_n = int(max(data[:, 0]))
train_ratio = 0.5
gamma = 1
lamb = 5
theta = np.zeros(d)
beta = 1
V = lamb * np.eye(d)
#ldV = np.linalg.slogdet(V)[1]
X = np.zeros((1, d), dtype = np.float)
Y = np.zeros(1)
x_feature = np.zeros((pool_size,d), dtype = np.float)
UCB = np.zeros(pool_size, dtype = np.float)
session = np.zeros(session_n, dtype = np.float)
K = 5
click_n = 0

idx = np.random.permutation(session_n) +1
tr_idx = idx[:int(round(session_n * train_ratio))]
ts_idx = idx[int(round(session_n * train_ratio)):]
#tr = session[idx[0:round(session_n * train_ratio)]]
#ts = session[idx[round(session_n * train_ratio)]+1:session_n]

#train
app = app[:,1:]
delta = 1/np.sqrt(tr_idx.shape[0])
for i in range(tr_idx.shape[0]):
    
    record = data[np.where(data[:, 0] == tr_idx[i])]
    u = user[np.where(user[:, 0] == record[0, 0])][0,1:]
    for a in range(pool_size):
        x_feature[a] = np.outer(u, app[a, :]).reshape(1, d)
        x_feature[a] = np.divide(x_feature[a], np.linalg.norm(x_feature[a]))
        UCB[a] = utils.getUCB(theta, x_feature[a], beta, V)
    action = UCB.argsort()[-K:][::-1]
    reward = match_app.match(record, action)
    if reward is not None:
        idx = np.array(reward.keys())
        x_t = x_feature[idx, :]
        w = np.array(reward.values()).reshape(x_t.shape[0])
    else:
        continue
    [V, X, Y, theta, beta] = utils.update_stat(V, x_t, X, Y, w, lamb, delta)


#test
delta = 1/np.sqrt(ts_idx.shape[0])
for i in range(ts_idx.shape[0]):
    record = data[np.where(data[:, 0] == ts_idx[i])]
    u = user[np.where(user[:, 0] == record[0, 0])][0,1:]
    for a in range(pool_size):
        x_feature[a] = np.outer(u, app[a, :]).reshape(1, d)
        x_feature[a] = np.divide(x_feature[a], np.linalg.norm(x_feature[a]))
        UCB[a] = utils.getUCB(theta, x_feature[a], beta, V)
    action = UCB.argsort()[-K:][::-1]
    reward = match_app.match(record, action)
    if reward is not None:
        idx = np.array(reward.keys())
        x_t = x_feature[idx,:]
        w = np.array(reward.values()).reshape(x_t.shape[0])
    else:
        continue
    [V, X, Y, theta, beta] = utils.update_stat(V, x_t, X, Y, w, lamb, delta)
    click_n = click_n + utils.get_reward(w)

result = click_n / session_n*K
print "the reward is: %s" % result