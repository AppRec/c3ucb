# c3ucb

1. `app_util` contains some functions for extracting categories, labels and app_ids of all apps.
2. `extract_app` uses the above functions and output apps' numerical feature to output file.

# experiment
- `randomRec.py` computes CTR of random recommendation.
- data file's directory need to be changed

##TODOS
1. change all UCB update function to unbound version in 'main'
2. In `main_no_user`, ctr is computed from all valid session or only those training data? test part remain unchanged?
