import io
import app_util
# apps is a dictionary
# category1 and category2 are dictionarys 
# labels is a list

apps = app_util.find_app_pool()
print 'finish reading applist......'
app_file = '../combine_AppInfo.txt'
category1 = app_util.app_category_num(app_file, 1)
category2 = app_util.app_category_num(app_file, 2)
print 'finish calculate category......'
labels = app_util.app_labels(app_file)
outfile = open('../app_feature_origin.txt','w+')
processed_data = []
with io.open (app_file, mode='r', encoding='utf-8') as f:
    print "appInfo_sample opened..."
    for line in f:
        #print line
        app_feature = []
        line = line.strip().split('\t')
        if (len(line) != 7):
            print "line seperated with error."
            continue
        else:
            #print "line seperated sucessfully."
            try:
                app_id = apps[line[0]]
            except KeyError:
                #print "this app is not in the list"
                continue
            else:
                app_size = int(line[4])
                app_feature.append(app_id)
                app_feature.append(app_size)
                for key in category1:
                    if (key == line[3]):
                        app_feature.append(1)
                    else:
                        app_feature.append(0)
                for key in category2:
                    if line[5].find(key) >= 0:  # key in the category_2 of this app
                        app_feature.append(1)
                    else:
                        app_feature.append(0)

                if line[6] == 'null':
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
                #print "current app feature: %s" % app_feature
                processed_data.append(app_feature)
                print "len of proccessed data: %d" % len(processed_data)
    
    # rank processed_data by appid (0..n-1)
    processed_data.sort(key = lambda x : x[0])
    
    # normalize the value of app size
    max_size = max(row[1] for row in processed_data)
    min_size = min(row[1] for row in processed_data)
    for line in processed_data:
        line[1] = round((line[1]-min_size)/(max_size-min_size),3)
        for feature in line:
           outfile.write(str(feature) + ',')
        outfile.write('\n')
    print "len of processed data: %d" % len(processed_data)
    print "one of the app feature: %s" % processed_data[3]
    print "there are %d apps." % len(processed_data)
    print "len of each app feature: %d" % len(processed_data[3])
outfile.close()

             
                                       
