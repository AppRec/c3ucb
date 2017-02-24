import sys
import time

def main():
    #read in file
    data = []
    aid_dict ={}
    app_dict = {}
    position_dict = {}
    with open("../session.txt", "r") as f:
        for line in f:
            line = line.strip().rstrip(',').split(',')
            line = list(map(int, line))
            data.append(line)
        f.close()
    with open('../applist.txt','r')  as f:
        for line in f:
            l = line.strip().split(',')
            l[1] = int(l[1])
            if l[1] not in aid_dict:
                aid_dict[l[1]] = l[0]
        f.close()
    #print(aid_dict)
    
    for row in data:
        aid = aid_dict[row[1]]
        if aid in app_dict:
            app_dict[aid][0]+=1
            if(row[2]==11 or row[2]==10):
                app_dict[aid][1]+=1
        else:
            info=[]
            info.append(1)
            if(row[2]==61):
                info.append(0)
            else:
                info.append(1)
            app_dict[aid] = info
        # if row[1] in app_dict:
            # app_dict[row[1]][0]+=1
            # if(row[2]==11 or row[2]==10):
                # app_dict[row[1]][1]+=1
        # else:
            # info=[]
            # info.append(1)
            # if(row[2]==61):
                # info.append(0)
            # else:
                # info.append(1)
            # app_dict[row[1]] = info
            
        if row[-1] in position_dict:
            position_dict[row[-1]][0]+=1
            if(row[2]==11 or row[2]==10):
                position_dict[row[-1]][1]+=1
        else:
            info = []
            info.append(1)
            if(row[2]==61):
                info.append(0)
            else:
                info.append(1)
            position_dict[row[-1]] = info
            
            
    with open('../LogFile/app_ctr.txt','a') as f1:
        f1.write('*'*20)
        for app in app_dict:
            app_ratio = float(app_dict[app][1])/app_dict[app][0]
            app_dict[app].append(app_ratio)
            f1.write(str(app) + ',' + str(app_dict[app][0]) + ',' + str(app_dict[app][1]) + ',' + str(app_dict[app][2]))
            f1.write('\n')
        f1.close()
    with open('../LogFile/pos_ctr.txt','a') as f2:
        f2.write('*'*20)
        for pos in position_dict:
            p_ratio = float(position_dict[pos][1])/position_dict[pos][0]
            position_dict[pos].append(p_ratio)
            f2.write(str(pos) + ',' + str(position_dict[pos][0]) + ',' + str(position_dict[pos][1]) + ',' + str(position_dict[pos][2]))
            f2.write('\n')
        f1.close()
    
if __name__ == '__main__':
    main()
