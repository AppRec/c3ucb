#!/bin/sh

# execute following command before running:
# chmod +x test.sh
# ./test.sh
cd ~/c3ucb

# output to: applist.txt
python app_util.py

# extract features and sessions
# output: app_feature_origin.txt
python extract_app.py
# output: 
python extract_session_data_v2.py
# output: user_feature_origin.txt
python extract_user_data_v2.py

# use pca to reduce feature dimension
# input: user_feature_origin.txt, app_feature_origin.txt
# output: user_feature.txt, app_feature.txt
python PCA.py

# main function
python main.py


# bootstrap main function
# python BT.py
# python main_BT.py


# main function: reccommend without user feature
# python main_no_user.py 

