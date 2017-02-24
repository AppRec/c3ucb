#encoding=utf-8
import sys
import time

def main():
    #read in file
    data = []
    name_dict = {}
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
    with open('../combine_AppInfo.txt','r') as f:
        for line in f:
            l = line.strip().split('\t')
            if l[0] not in name_dict:
                name_dict[l[0]] = unicode(l[2]).encode('utf-8')
        f.close()
    
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
            info.append(name_dict[aid])
            app_dict[aid] = info
        
            
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
           
            
    with open('../LogFile/app_ctr.txt','w') as f1:
        f1.write('*'*20+'\n')
        for app in app_dict:
            app_ratio = float(app_dict[app][1])/app_dict[app][0]
            app_dict[app].append(app_ratio)
        app_dict = sorted(app_dict.items(), key = lambda x:x[1][2], reverse = True)
        for app in app_dict:
            #f1.write(str(app) + ',' + str(app_dict[app][0]) + ',' + str(app_dict[app][1]) + ',' + str(app_dict[app][2]))
            f1.write(str(app).decode('utf-8'))
            f1.write('\n')
        f1.close()
    with open('../LogFile/pos_ctr.txt','w') as f2:
        f2.write('*'*20+'\n')
        for pos in position_dict:
            p_ratio = float(position_dict[pos][1])/position_dict[pos][0]
            position_dict[pos].append(p_ratio)
        position_dict = sorted(position_dict.items(), key = lambda x:x[1][2], reverse = True)
        for pos in position_dict:  
            #f2.write(str(pos) + ',' + str(position_dict[pos][0]) + ',' + str(position_dict[pos][1]) + ',' + str(position_dict[pos][2]))
            f2.write(str(pos))
            f2.write('\n')
        f1.close()
    
if __name__ == '__main__':
    main()
