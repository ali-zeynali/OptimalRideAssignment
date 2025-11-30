import numpy as np
import json

from MyAlg import *

driver_move_range = [0.01, 0.01]

distance_options = [1, 2, 5, 10, 15, 30]
max_waiting_list = 100
utilities = [np.log2(d / distance_options[0]) for d in distance_options]



data = {}

for alpha in [0, 0.5, 1]:
    deadhead_distances = []
    unassigned_values = []
    data[alpha] = {}
    for q in range(max_waiting_list + 10):
        algorithm = MyAlg(driver_move_range=driver_move_range, distance_options=distance_options,
                          max_waiting_list=max_waiting_list, alpha=alpha, V_coeff=1, lr=0)
        algorithm.utility_function = utilities
        algorithm.d0 = 0
        unassigned_requests = q
        d = algorithm.calculate_limit(unassigned_requests)
        deadhead_distances.append(d)
        unassigned_values.append(q)


    data[alpha]['d'] = deadhead_distances
    data[alpha]['n'] = unassigned_values

with open('results/Understanding/d_vs_q.json', 'w') as writer:
    json.dump(data, writer)

###########################

utilities = [np.log2(d / distance_options[0]) for d in distance_options]



data = {}

for alpha in [0, 0.5, 1]:
    deadhead_distances = []
    Q_max_vals = []
    data[alpha] = {}
    # for q_max in range(5, 21, 1):
    for q_max in range(10, 101, 5):
        algorithm = MyAlg(driver_move_range=driver_move_range, distance_options=distance_options,
                          max_waiting_list=q_max, alpha=alpha, V_coeff=1, lr=0)
        algorithm.utility_function = utilities
        algorithm.d0 = 0
        # unassigned_requests = 5
        unassigned_requests = 15
        d = algorithm.calculate_limit(unassigned_requests)
        deadhead_distances.append(d)
        Q_max_vals.append(q_max)


    data[alpha]['d'] = deadhead_distances
    data[alpha]['Q'] = Q_max_vals

with open('results/Understanding/d_vs_Qmax.json', 'w') as writer:
    json.dump(data, writer)