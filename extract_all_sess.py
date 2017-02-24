#l[0]<- uid, l[1]<- appid, l[2]<- date&time, l[3]<- oper_type, l[4]<- category, l[5]<- '', l[6]<- listid, l[7]<- position
import sys
import time

processed_data = []
processed_data2 = []
optype_dict = {}
app_dict = {}
user_dict = {}

mydate = 20161100
record_counter = 0
user_counter = 0
start = time.clock()
t=0
days = 15
for i in range(0,days):
    #print 'Start at time: %.3f'%(time.clock()-start)
    mydate += 1
    #filename = '../DataFile/Data_randomHiad_' + str(mydate) + '.txt'
    filename = './Data_randomHiad_' + str(mydate) + '.txt'
    with open(filename,'r') as f:
        data = f.readlines();
        record_counter += len(data)
        for line in data:
            l = line.strip().split('\t')
            #delete rows where position<3 && position>7 and category='HiAd'in list = 2
            if l[4] != 'HiAd' or l[6] != '2' or int(l[7])<3 or int(l[7])>7:#HiAd
                continue
            #delete date&time, HiAd;
            del l[2]
            del l[3]
            del l[3]
            processed_data.append(l)
        f.close()	
print ("There are: ",record_counter,"rows")
#print 'Session Loaded at: %.3f'%(time.clock()-start)
for line in processed_data:
    processed_data2.append(line)
#print 'Operation filtering completed at: %.3f'%(time.clock()-start)

#replace appID according to applist.txt
with open("../applist.txt",'r') as f2:
    #print '%.3f'%(time.clock()-start)
    data = f2.readlines()
    for line in data:
        l = line.strip().split(',')
        if l[0] not in app_dict:
            app_dict[l[0]] = l[1]
        #else:
            #print("repeated app id")
            #print "repeated app id"
    f2.close()
for i in range(0,len(processed_data2)):
    processed_data2[i][1] = app_dict[processed_data2[i][1]]
#print 'applist Loaded at: %.3f'%(time.clock()-start)
    
for line in processed_data2:
    if line[0] not in user_dict: 
        user_dict[line[0]] = user_counter
        user_counter += 1
for i in range(0,len(processed_data2)):
    processed_data2[i][0] = user_dict[processed_data2[i][0]] 
#print 'userlist Loaded at: %.3f'%(time.clock()-start)	
print ('User amount is: ', user_counter)
	
#print(processed_data2)
with open("../session_all.txt", 'w') as f1:
    #print '%.3f'%(time.clock()-start)
    for line in processed_data2:
        for e in line:
            f1.write(str(e))
            f1.write(',')
        f1.write('\n')
    f1.close()
#print 'session.txt outputed at: %.3f'%(time.clock()-start)