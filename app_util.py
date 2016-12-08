#! usr/bin/python
# encoding issues: Hiad.txt can only open with 'utf-16'
import io
'''
find from session record the apps exist in list 2, position 3~7
'''
def find_app_pool(filename):
    apps = []
    uniq_apps=[]
    with io.open (filename,mode='r',encoding='utf-8') as f:
        f.readline()
        for line in f:
            try:
                device_id, app_id, date, oper_type, Hiad, blank, listid, position = line.strip().split('\t')
            except ValueError:
                continue
            try:
                mainPage = int(listid)
                pos = int(position)
            except ValueError:
                continue
            else:
                if (mainPage == 2):
                    if (pos >=3 and pos <= 7):
                        apps.append(app_id)

    # print("the length of list of app is: {}".format(len(apps)))
    seen = set()
    for x in apps:
        if x not in seen:
            seen.add(x)
            uniq_apps.append(x)
    # print("the length of unique list is: {}".format(len(uniq_apps)))
    index = 1
    app_dict = {}
    for i in uniq_apps:
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
    session_file = 'rand_Hiad.txt'
    app_pool = find_app_pool(session_file)
    with io.open('app_index.txt',mode='wb') as f:
       index = 1
       for app in app_pool:
           f.write(str(app) + ',' + str(index) + '\n')
           index += 1

    # print(app_pool)

    app_file = 'app_feature.txt'
    cat_1 = app_category_num(app_file, 1)
    # print(cat_1)

    labels = app_labels(app_file)
    print(labels)

if __name__ == '__main__':
    main()
