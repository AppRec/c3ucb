# -*- coding: utf-8 -*-
#!/usr/bin/python

import numpy as np

'''
@param 
session
action
'''
def match(session, action):
	match_record = [-1 for i in range(len(action))]
	match_kv = dict()
	for line in session:
		for i in range(len(action)):
			if (line[1] == action[i]):
				if (int(line[2]) == 61):
					match_record[i] = 0
				elif (int(line[2]) == 11 or int(line[2]) == 10):
					match_record[i] = 1
	# print match_record
	try:
		# find the position of last click/down feedback
		stop_pos = len(action) - 1 - match_record[::-1].index(1)
	except ValueError:
		stop_pos = -1
	# print 'stop position: %d' % stop_pos
	if (stop_pos < 0): return None
	for i in range(stop_pos+1):
		if match_record[i] != -1:
			match_kv[action[i]] = match_record[i] 

	return match_kv


def main():
	session = np.array([[1,11,61,2,4],
						[1,18,11,2,5],
						[1,1,61,2,6],
						[1,9,11,2,5],
						[1,2,10,2,5],
						[1,3,61,2,5],
						[1,4,61,2,5],
						[1,5,61,2,5]])
	action_1 = np.array([3,4,5,6,9])
	action_2 = np.array([9,32,2,45,5])
	action_3 = np.array([3,4,5,3,3])
	print match(session, action_1)
	print match(session, action_2)
	print match(session, action_3)

if __name__ == '__main__':
	main()