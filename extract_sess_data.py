#replace appID; delete date&time, HiAd;
#keep records of a same user where at least 1 oper_type == 11||10
#delete rows where position<3 && position>7 in list = 2
import sys

processed_data = []
processed_data2 = []
#sdict = {}
optype_dict = {}
app_dict = {}
user_dict = {}
#app_counter = 0
with open("fsession.txt",'r') as f:
    data = f.readlines();
    for line in data:
        l = line.strip().split('\t')
        if int(l[5]) != 2 or int(l[6])<3 or int(l[6])>7:
            continue
        del l[2]
        del l[3]
        processed_data.append(l)
    f.close()	
	
for line in processed_data:
    if line[0] not in optype_dict:
        optype_dict[line[0]] = line[2]
    if int(line[2]) < int(optype_dict[line[0]]):
        optype_dict[line[0]] = int(line[2])
    #if line[1] not in sdict:
    #   app_counter += 1
    #   sdict[line[1]] = app_counter

for line in processed_data:
    if int(optype_dict[line[0]]) == 61:
        continue
    #line[1] = sdict[line[1]]
    #line[1] = str(line[1])
    processed_data2.append(line)

with open("applist.txt",'r') as f2:
    data = f2.readlines()
    for line in data:
        l = line.strip().split(',')
        if l[0] not in app_dict:
            app_dict[l[0]] = l[1]
        else:
            print("repeated app id")
            #print "repeated app id"
    f2.close()
for i in range(0,len(processed_data2)):
    processed_data2[i][1] = app_dict[processed_data2[i][1]]

with open("userlist.txt",'r') as f3:
    data = f3.readlines()
    for line in data:
        l = line.strip().split(',')
        if l[0] not in user_dict:
            user_dict[l[0]] = l[1]
        else:
            print("repeated user id")
            #print "repeated user id"
	f3.close()
for i in range(0,len(processed_data2)):
	processed_data2[i][0] = user_dict[processed_data2[i][0]] 	
	
#print(processed_data2)
with open("session.txt", 'w') as f1:
	for line in processed_data2:
		for e in line:
			f1.write(e)
			f1.write(',')
		f1.write('\n')
	f1.close()
		