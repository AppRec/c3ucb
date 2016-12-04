#! usr/bin/python
# encoding issue: first line of app_feature.txt contains utf-16 code
import app_util

# apps is a dictionary
# category1 and category2 are dictionarys 
# labels is a list
apps = app_util.find_app_pool('rand_Hiad.txt')
app_file = 'app_feature.txt'
category1 = app_util.app_category_num(app_file, 1)
category2 = app_util.app_category_num(app_file, 2)
labels = app_util.app_labels(app_file)
outfile = open('extracted_app_feature.txt','w+')

with open (app_file, 'r', encoding='utf-8') as f:
    for line in f:
        app_feature = []
        line = line.strip().split('\t')
        if (len(line) != 7):
            continue
        else:
            try:
                app_id = apps[line[0]]
            except KeyError:
                continue
            else:
                app_size = int(line[4])
                app_feature.append(app_id)
                app_feature.append(app_size)
                for key in category1:
                    # print (key, line[3])
                    # print(key == line[3])
                    if (key == line[3]):
                        app_feature.append(1)
                    else:
                        app_feature.append(0)
                for key in category2:
                    if (line[5].find(key) >= 0):  # key in the category_2 of this app
                        app_feature.append(1)
                    else:
                        app_feature.append(0)
                
                if (line[6] == 'null'):
                    app_feature += len(labels) * [0]
                else:
                    pairs = line[6].split(' ') 
                    for label in labels:
                        matched = False
                        for p in pairs:
                            p = p.split(':')
                            if (label == p[0]):
                                app_feature.append(float(p[1]))
                                matched = True
                                break
                        if (not matched):
                            app_feature.append(0)
        for feature in app_feature:
            outfile.write(str(feature) + ',')
        outfile.write('\n')
        # print (app_feature)
        
