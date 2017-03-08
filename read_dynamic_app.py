#l[0]<- uid, l[1]<- appid, l[2]<- date&time, l[3]<- oper_type, l[4]<- category, l[5]<- '', l[6]<- listid, l[7]<- position
import sys
import os

mydate = 20161100
days = 30
app_pool = {}
whole_pool = []
whole_pool2 = []
app_counter = 0
for i in range(0,days):
    mydate += 1
    filename = '../DataFile/Data_randomHiad_' + str(mydate) + '.txt'
    #filename = './Data_randomHiad_' + str(mydate) + '.txt'
    if os.path.exists(filename) == False:
        print 'skip day: %s' % str(mydate)
        continue
    daily_pool = {}
    daily_pool2 = []
    #daily_counter = 0
    with open(filename,'r') as f:
        data = f.readlines();
        for line in data:
            l = line.strip().split('\t')
            #record new app into app_pool
            if l[1] not in app_pool:
                app_pool[l[1]] = 1
                app_counter += 1
            else:
                app_pool[l[1]] += 1
                
            #record the app into daily statistic
            if l[1] not in daily_pool:
                daily_pool[l[1]] = 1
                daily_pool2.append(l[1])
                #daily_counter += 1
        f.close()	
    whole_pool.append(daily_pool)
    whole_pool2.append(daily_pool2)

#for finding the intersection set and corresponding size of 2 adjacent days
# inter = list(set(whole_pool2[0]).intersection(set(whole_pool2[1])))
# inter = list(set(whole_pool2[0]).difference(set(whole_pool2[1])))
# print(inter)
# print(len(inter))

with open('../LogFile/dynamic_app_info.txt','w') as f:
    f.write('Date')
    f.write('\t')
    for app in app_pool:
        f.write(app)
        f.write('\t')
    f.write('Total')
    f.write('\n')
    for i in range(0,days):
        f.write('11_%02d' % i)
        f.write('\t')
        for j in app_pool:
            if j in whole_pool[i]:
                f.write('1')
                f.write('\t')
            else:
                f.write('0')
                f.write('\t')
        daily_amount = len(whole_pool[i])
        f.write(str(daily_amount))
        f.write('\n')
    f.write('Total')
    f.write('\t')
    for app in app_pool:
        f.write(str(app_pool[app]))
        f.write('\t')
    f.close()
