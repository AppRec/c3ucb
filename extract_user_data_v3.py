#search_word converted to number; get set of download_app && used app && searched apps 
#convert model to number
#uid0	type1	used_app3	download_app2	search_word4 
#coding:utf-8
import sys
import numpy as np
import math
import io
import time

data = []
processed_data = []
type_dict = {}
aid_dict = {}
search_dict = {}
user_dict = {}
user_counter=0
type_counter=0
aid_counter=0
search_counter=0
type_dict["Null"]=0
aid_dict["Null"]=0
search_dict["Null"]=0

start = time.clock()
t=0

#read the list of user
with open("../userlist.txt",'r') as f:
    print 'Start at time: %.3f'%(time.clock()-start)
    data = f.readlines()
    for line in data:
        l = line.strip().split(',')
        if l[0] not in user_dict:
            user_dict[l[0]] = l[1]
    f.close()
    
#read the user-feature dataset and filter the ones did not appear in the session data
with io.open("../Result_use_down_search_20161030.txt",'r', encoding='UTF-8') as f:
    print 'Start to load user time: %.3f'%(time.clock()-start)
    #data = f.readlines();
    for line in f:
        if int(time.clock()-start) / 30 > t:
            t = int(time.clock()-start) / 30
            #print '30 seconds left'
        l = line.strip().split('\t')
        
        if l[0] not in user_dict:
            continue
        user_counter += 1
        
        used_apps = l[2].split(',') 
        download_apps = l[3].split(',')
        search_apps = l[4].split(',')

        if l[1] not in type_dict:
            type_counter += 1
            type_dict[l[1]] = type_counter
        #get set of download_app && used app && searched apps 
        for i in used_apps:	
            if i not in aid_dict:
                aid_counter += 1
                aid_dict[i] = aid_counter
        for i in download_apps:		
            if i not in aid_dict:
                aid_counter += 1
                aid_dict[i] = aid_counter
        for i in search_apps:		
            if i not in search_dict:
                search_counter += 1
                search_dict[i] = search_counter
    f.close()		
del aid_dict['Null']
del search_dict['Null']
print 'Aid number is : %d' %(aid_counter)
print 'Users loaded at: %.3f'%(time.clock()-start)

with io.open("../Result_use_down_search_20161030.txt",'r', encoding='UTF-8') as f:
    for line in f:
        if int(time.clock()-start) / 30 > t:
                t = int(time.clock()-start) / 30
                #print '30 seconds left'
        l = line.strip().split('\t')
        if l[0] not in user_dict:
            continue
        used_apps = l[2].split(',') 
        download_apps = l[3].split(',')
        search_apps = l[4].split(',')
        newl=[]
        newl.append(user_dict[l[0]])
        newl.append(type_dict[l[1]])
        #convert download_app && used_app && search_word into binary variable
        for key in aid_dict:
            if key in used_apps:
                newl.append(1)
            elif key in download_apps:
                newl.append(0.5)
            else:
                newl.append(0)
        for key in search_dict:
            if key in search_apps:
                newl.append(1)
            else:
                newl.append(0)
        processed_data.append(newl)

max = max([row[1] for row in processed_data])
min = min([row[1] for row in processed_data])
print "Num of users: ", user_counter
print 'Filtering completed at %.3f'%(time.clock()-start)

with open("../user_feature_origin2.txt",'w') as f1:
    for line in processed_data:
        if int(time.clock()-start) / 30 > t:
                t = int(time.clock()-start) / 30
                #print '30 seconds left'
        #min-max normlization
        line[1] = round(float((line[1]-min)/(max-min)),3)
        line
        for i in line:
            f1.write(str(i))
            f1.write(',')
        f1.write('\n')
    print 'user_feature.txt outputed at: %.3f'%(time.clock()-start)
    f1.close()