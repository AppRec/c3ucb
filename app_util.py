'''
find the apps exist in list 2, position 3~7 from session record 
'''
import io
from os import path

def find_app_pool():
    d = 20161100
    apps = set()
    for i in range(30):
        d += 1
        filename = '../DataFile/Data_randomHiad_' + str(d) + '.txt'
        # check if file exists
	if not path.exists(filename): continue
        with io.open (filename,mode='r',encoding='utf-8') as f:
            #f.readline()
            for line in f:
                try:
                   # print(line)
                   device_id, app_id, date, oper_type, Hiad, blank, listid, position = line.strip().split('\t')
                   # print app_id
                except ValueError:
                    continue
                try:
                    mainPage = int(listid)
                    pos = int(position)
                    #print mainPage
                    #print pos
                except ValueError:
                    continue
                else:
                    if (mainPage == 2):
                        if (Hiad == 'HiAd'):
                            if (pos >=3 and pos <= 7):
                                apps.add(app_id)

        print "finish file %d" % i
    # print(apps)
    # print("the length of list of app is: {}".format(len(apps)))
    index = 0
    app_dict = {}
    for i in apps:
        app_dict[i] = index
        index += 1
    return app_dict

'''
assign a distinct number to each category_1 & category_2

'''
def app_category_num(filename, category_level):
    apps = set()
    app_dict = {}
    cnt = 0
    with io.open (filename,mode='r',encoding='utf-8') as f:
        if (category_level == 1):
            for line in f:
                l = line.strip().split('\t')
                if (len(l) != 7):
                    continue
                else:
                    apps.add(l[3]) # category_1 lies in 3rd column

        if (category_level == 2):
            for line in f:
                l = line.strip().split('\t')
                if (len(l) != 7):
                    continue
                else:
                    category_2 = l[5].split(" ") # category_2 lies in 5th column
                    for c in category_2:
                        if (c != 'null'):
                            apps.add(c)
        for app in apps:
                cnt += 1
                app_dict[app] = cnt
    return app_dict

def app_labels(filename):
    labels = set()
    with io.open (filename,mode='r',encoding='utf-8') as f:
        for line in f:
            l = line.strip().split('\t')
            if (len(l) != 7):
                continue
            elif (l[6] != 'null'):
                pairs = l[6].split(' ')
                for i in pairs:
                    label,weight = i.split(':')
                    labels.add(label)
    return list(labels)

def main():
    app_pool = find_app_pool()
    with open('../applist.txt', 'w') as f:
        for key in app_pool:
                f.write(str(key) + ',' + str(app_pool[key]) + '\n')
    
    # app_file = 'app_feature.txt'
    # cat_1 = app_category_num(app_file, 1)
    # # print(cat_1)
    #
    # labels = app_labels(app_file)
    # print(labels)

if __name__ == '__main__':
    main()                                                    
