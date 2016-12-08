#replace appID; delete date&time, HiAd;
#keep records of a same user where at least 1 oper_type == 11||10
#delete rows where position<3 && position>7 in list = 2
import sys
import time

processed_data = []
processed_data2 = []
optype_dict = {}
app_dict = {}
user_dict = {}

date = 20161100
record_counter = 0
start = time.clock()
for i in range(0,6):
    print '%.3f'%(time.clock()-start)
    date += 1
    filename = '../DataFile/Data_randomHiad_' + str(date) + '.txt'
    with io.open(filename,'r') as f:
        data = f.readlines();
        record_counter += len(data)
        for line in data:
            l = line.strip().split('\t')
            if int(l[5]) != 2 or int(l[6])<3 or int(l[6])>7:
                continue
            del l[2]
            del l[3]
            processed_data.append(l)
        f.close()	
print "There are: ",record_counter,"rows"
	
for line in processed_data:
    if line[0] not in optype_dict:
        optype_dict[line[0]] = line[2]
    if int(line[2]) < int(optype_dict[line[0]]):
        optype_dict[line[0]] = int(line[2])
print '%.3f'%(time.clock()-start)

for line in processed_data:
    if int(optype_dict[line[0]]) == 61:
        continue
    processed_data2.append(line)

with io.open("../applist.txt",'r') as f2:
    print '%.3f'%(time.clock()-start)
    data = f2.readlines()
    for line in data:
        l = line.strip().split(',')
        if l[0] not in app_dict:
            app_dict[l[0]] = l[1]
        else:
            #print("repeated app id")
            print "repeated app id"
    f2.close()
for i in range(0,len(processed_data2)):
    processed_data2[i][1] = app_dict[processed_data2[i][1]]

with io.open("../userlist.txt",'r') as f3:
    print '%.3f'%(time.clock()-start)
    data = f3.readlines()
    for line in data:
        l = line.strip().split(',')
        if l[0] not in user_dict:
            user_dict[l[0]] = l[1]
        else:
            #print("repeated user id")
            print "repeated user id"
    f3.close()
for i in range(0,len(processed_data2)):
    processed_data2[i][0] = user_dict[processed_data2[i][0]] 	
	
#print(processed_data2)
with io.open("../session.txt", 'wb') as f1:
    print '%.3f'%(time.clock()-start)
    for line in processed_data2:
        for e in line:
            f1.write(e)
            f1.write(',')
        f1.write('\n')
    f1.close()
		