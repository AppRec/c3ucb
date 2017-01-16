#search_word converted to number; get set of download_app && used app && searched apps 
#convert model to number
#uid0	type1	download_app2	used_app3	search_word4 
#coding:utf-8
import sys
import numpy as np
import math
import io
import time

data = []
processed_data = []
type_dict = {}
used_dict = {}
dl_dict = {}
search_dict = {}
user_dict = {}
user_dict2 = {}
user_counter=0
type_counter=0
used_counter=0
dl_counter=0
search_counter=0
type_dict["Null"]=0
used_dict["Null"]=0
dl_dict["Null"]=0
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
            print '30 seconds left'
        l = line.strip().split('\t')
        
        if l[0] not in user_dict:
            continue
        user_dict2[l[0]] = user_counter
        user_counter += 1
        download_apps = l[2].split(',') 
        used_apps = l[3].split(',')
        search_apps = l[4].split(',')

        if l[1] not in type_dict:
            type_counter += 1
            type_dict[l[1]] = type_counter
        #get set of download_app && used app && searched apps 
        for i in used_apps:	
            if i not in used_dict:
                used_counter += 1
                used_dict[i] = used_counter
        for i in download_apps:		
            if i not in dl_dict:
                dl_counter += 1
                dl_dict[i] = dl_counter
        for i in search_apps:		
            if i not in search_dict:
                search_counter += 1
                search_dict[i] = search_counter
    f.close()		
del dl_dict['Null']
del used_dict['Null']
del search_dict['Null']
print 'Users loaded at: %.3f'%(time.clock()-start)

with io.open("../Result_use_down_search_20161030.txt",'r', encoding='UTF-8') as f:
    for line in f:
        if int(time.clock()-start) / 30 > t:
                t = int(time.clock()-start) / 30
                print '30 seconds left'
        l = line.strip().split('\t')
        if l[0] not in user_dict:
            continue
        download_apps = l[2].split(',') 
        used_apps = l[3].split(',')
        search_apps = l[4].split(',')
        newl=[]
        newl.append(user_dict2[l[0]])
        newl.append(type_dict[l[1]])
        #convert download_app && used_app && search_word into binary variable
        for key in dl_dict:
            if key in download_apps:
                newl.append(1)
            else:
                newl.append(0)
        for key in used_dict:
            if key in used_apps:
                newl.append(1)
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

with open("../user_feature_origin.txt",'w') as f1:
    # f1.write("uid")
    # f1.write(',')
    # f1.write("device_type")
    # f1.write(',')
    # for key in dl_dict:
        # f1.write(key)
        # f1.write(',')
    # for key in used_dict: 
        # f1.write(key)
        # f1.write(',')
    # for key in search_dict:
        # f1.write(key)
        # f1.write(',')
    # f1.write('\n')
    for line in processed_data:
        if int(time.clock()-start) / 30 > t:
                t = int(time.clock()-start) / 30
                print '30 seconds left'
        #min-max normlization
        line[1] = round(float((line[1]-min)/(max-min)),3)
        for i in line:
            f1.write(str(i))
            f1.write(',')
        f1.write('\n')
    print 'user_feature.txt outputed at: %.3f'%(time.clock()-start)
    f1.close()
