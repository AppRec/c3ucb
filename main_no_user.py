"""
in this version of c3-ucb, user features are not used,
Apps are recommended only based on app feature.
"""
import numpy as np
import match_app
import utils
from time import strftime, localtime

def main(lamb, R):
    #read in file
    tmp = []
    with open("../session.txt", "r") as f:
        for line in f:
            line = line.strip().rstrip(',').split(',')
            line = list(map(float, line))
            tmp.append(line)
        f.close()
    data = np.asarray(tmp)
    tmp=[]

    # with open("../user_feature.txt", "r") as f:
    #     for line in f:
    #         line = line.strip().rstrip(',').split(',')
    #         line = list(map(float, line))
    #         tmp.append(line)
    #     f.close()
    # user = np.asarray(tmp)
    # tmp=[]

    with open("../app_feature.txt", "r") as f:
        for line in f:
            line = line.strip().rstrip(',').split(',')
            line= list(map(float, line))
            tmp.append(line)
        f.close()
    app = np.asarray(tmp)

    #initialization
    pool_size = app.shape[0]
    #user_row_n = user.shape[1]
    app_row_n = app.shape[1]
    d = app_row_n - 1  #d = int((user_row_n-1)*(app_row_n-1))
    session_n = int(max(data[:, 0]))
    train_ratio = 0.7
    gamma = 1
    # lamb = 0.5
    theta = np.zeros(d)
    beta = 1
    delta = 0.9
    V = lamb * np.eye(d)
    X = np.zeros((1, d), dtype = np.float)
    Y = np.zeros(1)
    x_feature = np.zeros((pool_size,d), dtype = np.float)
    UCB = np.zeros(pool_size, dtype = np.float)
    session = np.zeros(session_n, dtype = np.float)
    K = 5
    click_n = 0

    idx = np.random.permutation(session_n)
    tr_idx = idx[:int(round(session_n * train_ratio))]
    ts_idx = idx[int(round(session_n * train_ratio)):]

    # open file for storing log info 
    cur_time = strftime("%Y%m%d_", localtime())
    logFileName = '../LogFile/main_no_user_' + cur_time + '.txt'
    logFile = open(logFileName, 'a+')
    print >>logFile, '\n\n'
    print >>logFile, '='*50
    print >>logFile, 'experiment parameters: lambda=%f, R=%f' % (lamb, R)
    print >>logFile, '\n\n'


    #train
    app = app[:,1:]
    expl = np.zeros(pool_size)
    for i in range(tr_idx.shape[0]):
        record = np.zeros(1)
        #u = np.zeros(1)
        try:
            record = data[np.where(data[:, 0] == tr_idx[i])]
            #u = user[np.where(user[:, 0] == record[0, 0])][0,1:]
        except IndexError:
            continue
        else:
            for a in range(pool_size):
                #x_feature[a] = np.outer(u, app[a, :]).reshape(1, d)
                x_feature[a] = app[a, :]
                x_feature[a] = np.divide(x_feature[a], np.linalg.norm(x_feature[a]))
                UCB[a] = utils.getUCB(theta, x_feature[a], beta, V)
                # print "this is app "+str(a)+" UCB is " + str(UCB[a])
            action = UCB.argsort()[-K:][::-1]
            for ii in range(K):
                if expl[action[ii]] == 0:
                    expl[action[ii]] = 1
            # print expl
            reward = match_app.match(record, action)
            idx=[]
            val=[]
            if reward is not None:
                for j in reward:
                    if reward[j]==1 or reward[j]==0:
                        idx.append(j)
                        val.append(reward[j])

                idx = np.asarray(idx)
                val = np.asarray(val)
                x_t = x_feature[idx,:]
                w = np.array(val.reshape(x_t.shape[0],1))
                #print w
                [V, X, Y, theta, beta] = utils.update_stat(V, x_t, X, Y, w, lamb, delta, R)

            else:
                continue
    #test
    cnt = 0
    result = [0]
    for i in range(ts_idx.shape[0]):
        record = np.zeros(1)
        #u = np.zeros(1)
        try:
            record = data[np.where(data[:, 0] == ts_idx[i])]
            #u = user[np.where(user[:, 0] == record[0, 0])][0,1:]
        except IndexError:
            continue
        else:
            for a in range(pool_size):
                #x_feature[a] = np.outer(u, app[a, :]).reshape(1, d)
                x_feature[a] = app[a, :]
                x_feature[a] = np.divide(x_feature[a], np.linalg.norm(x_feature[a]))
                UCB[a] = utils.getUCB(theta, x_feature[a], beta, V)
                #print "this is app "+str(a)+" UCB is " + str(UCB[a])
            action = UCB.argsort()[-K:][::-1]
            for ii in range(K):
                if expl[action[ii]] == 0:
                    expl[action[ii]] = 1
            # print expl
            reward = match_app.match(record, action)
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
                x_t = x_feature[idx,:]
                w = np.array(val.reshape(x_t.shape[0],1))
                #print w
                [V, X, Y, theta, beta] = utils.update_stat(V, x_t, X, Y, w, lamb, delta, R)
                click_n = click_n + utils.get_reward(w)
                result.append((float(click_n)/cnt))
            else:
                continue


    print >>logFile, "the reward is: %s" % result
    print >>logFile, "cnt is: %s" % cnt
    expl_n = sum(expl)
    expl_n_rate = float(expl_n)/pool_size
    print >>logFile, "expl_n is %s" % str(expl_n)
    print >>logFile, "expl_rate is %s" % str(expl_n_rate)

    logFile.close()

if __name__ == '__main__':
    main(lamb=10, R=1)
    #main(lamb=50, R=1)
    #main(lamb=0.1, R=0.1)

