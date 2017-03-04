import numpy as np


def match(session, action):
    """
    find matched apps in the session and return all of them no matter click/down or not.
    return None if all apps in action cannot match.
    Parameters:
    session - a numpy nd-array
    action - a numpy array containing recommended apps
    """
    match_record = [-1 for i in range(len(action))]
    match_kv = dict()
    for line in session:
        for i in range(len(action)):
            if (line[1] == action[i]):
                #print "matched %f and %d" % (line[1],action[i])
                if (int(line[2]) == 61 and match_record[i] == -1):
                    match_record[i] = 0
                elif (int(line[2]) == 11 or int(line[2]) == 10):
                    match_record[i] = 1
    # print match_record
    for i in range(len(action)):
        if match_record[i] != -1:
            match_kv[action[i]] = match_record[i]

    if not match_kv:
        return None
    return match_kv

def get_all_ctr(appListFile, appCtrFile):
    listF = open(appListFile,'r') # 459 apps in total
    ctrF = open(appCtrFile,'r') # 412 apps in total(in valid session)
    apps = dict() # key: app name, value: app index
    appCtr = dict() # key: app index, value: ctr

    for line in listF:
        l = line.strip().split(',')
        apps[l[0]] = int(l[1])
    listF.close()

    for line in ctrF:
        l = line.strip().split(',')
        if len(l) == 4:
            app_idx = apps[l[0]]
            appCtr[app_idx] = float(l[-1])
    ctrF.close()

    return appCtr


def genCtr(action):
    """
    generate the action's reward based on apps' ctr
    """
    actReward = dict() # key: app idx, value: 0 or 1 

    appCtr = get_all_ctr(appListFile='../applist.txt', \
                         appCtrFile='../app_ctr.txt')

    for a in action:
        ctr = appCtr[a]
        
        val = np.random.choice(2, 1, p=[1-ctr, ctr]) 
        
        actReward[a] = val # P(val=1)==ctr, P(val=0)==1-ctr 

    return actReward



def main():
        session = np.array([[1,11.0,61,2,4],
                            [1.0,18.0,11.0,2.0,5.0],
                            [1,1.0,61,2,6],
                            [1,9,11,2,5],
                            [1,2,10,2,5],
                            [1,3,61,2,5],
                            [1,4,61,2,5],
                            [1,5,61,2,5]])
        # print session
        # in the action below, only appid=9 has click behaviour.
        action_1 = np.array([11,9,4,5,6])
        action_2 = np.array([9,11,4,5,6])
        action_3 = np.array([11,4,5,6,9])
        action_4 = np.array([80,81,82,83,84])
        print match(session, action_1)
        print match(session, action_2)
        print match(session, action_3)
        print match(session, action_4)

if __name__ == '__main__':
        main()


