import numpy as np
import sys
import random

data = []
#read session file
#with open("../session.txt", "r") as f:
with open("./session.txt", "r") as f:
    for line in f:
        line = line.strip().rstrip(',').split(',')
        # py2
        # data = map(float,data)
        # py3
        #print(line)
        line = list(map(float, line))
        data.append(line)
    f.close()
sess = np.asarray(data)
sess_amount = int(max(sess[:, 0]))

T = sess_amount; #related to user amount
B = 3;
for i in range(0,B):
    #filename = '../session_bootstrap' + str(i+1) + '.txt'
    filename = './session_bootstrap' + str(i+1) + '.txt'
    dictname = './sid_dict' + str(i+1) + '.txt'
    id_dict = {}
    with open(filename,'w') as f1:
        for j in range(0,T):
            sid = random.randint(1,sess_amount)
            if sid not in id_dict:
                id_dict[sid] = 1
            else:
                id_dict[sid] += 1
            record = sess[np.where(sess[:, 0] == sid)]
            for r in range(0,record.shape[0]):
                for c in range(0,record.shape[1]):
                    f1.write(str(record[r,c]))
                    f1.write(',')
                f1.write('\n')
        f1.close()
    with open(dictname,'w') as f2:
        for i in id_dict:
            f2.write(str(i))
            f2.write(',')
            f2.write(str(id_dict[i]))
            f2.write('\n')
        f2.close()
        
