import matplotlib.pyplot as plt
import numpy as np

daily_apps = []
with open('dynamic_app_info.txt', 'r') as f:
    data = f.readlines()
    for idx, line in enumerate(data):
        if idx==0:
            continue
        l = line.strip().split('       ')
        del l[0]
        if len(l)==0:
            continue
        l = list(map(int, l))
        daily_apps.append(l)
        #print idx
    f.close()

    #del daily_apps[0]
    
    #print (len(daily_apps))
    
    apps = np.asarray(daily_apps)
    
    #print(apps.shape)
    apps1 = apps[:,:-1]
    apps1[apps1==1] = 255
    print (apps1)
    #print(apps1.shape)
    fig, ax = plt.subplots()
    ax.imshow(apps, cmap="Greys", interpolation='nearest')
    plt.show()