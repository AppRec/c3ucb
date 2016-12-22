
import numpy as np
tmp = []
with open("session.txt", "r") as f:
    for line in f:
        line = line.strip().rstrip(',').split(',')
        line = list(map(float, line))
        tmp.append(line)
    f.close()
data = np.asarray(tmp)

session_n = int(max(data[:,0]))
cnt = 0
click_n = 0
current_session = None
current_app = None
Flag = False

for line in data:
    if not current_session:
        current_session = line[0]
        current_app = line[1]
        cnt += 1
        if line[2]==11 or line[2]==10:
            click_n += 1
            flag = True
    else:
        if line[0] == current_session:
            if line[1] == current_app:
                if (not flag) and (line[2] == 11 or line[2] == 10):
                    click_n += 1
                    flag = True
            else:
                flag = False
                current_app = line[1]
                cnt += 1
                if line[2] == 11 or line[2] == 10:
                    click_n += 1
                    flag = True
        else:
            flag = False
            current_session = line[0]
            current_app = line[1]
            cnt += 1
            if line[2]==11 or line[1]==10:
                click_n += 1
                flag = True

print "total number of click: %d" % click_n
print "total number of record: %d" % cnt
print "ctr = %f" % (float(click_n)/cnt)