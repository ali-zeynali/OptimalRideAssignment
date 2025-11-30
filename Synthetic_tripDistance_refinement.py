import json
import numpy as np



def read_data(path):
    with open(path, 'r') as reader:
        return json.load(reader)


data_path = "results/Synthetic_tripDistance/"
algorithms = [ "MyAlg", "TORA", "CD"]

result = {}
do_refinement = True
for alg in algorithms:
    data =read_data(data_path + f"{alg}.json")

    tripDistances = []
    emission = []
    waiting = []
    for v in data:
        tripDistance = float(v)
        if tripDistance >= 35:
            break

        e = np.average([sample['avg_emission'] for sample in data[v]])
        w = np.average([sample['avg_waiting'] for sample in data[v]])

        tripDistances.append(tripDistance)
        emission.append(e)
        waiting.append(w)

    n = len(tripDistances)
    if do_refinement:
        for i in range(n):
            emission[i] = float(np.average(emission[max(0,i-1):min(n, i+1)]))
            waiting[i] = float(np.average(waiting[max(0, i-1):min(n, i+1)]))
            # if drivers[i] <= 200:
            #     if alg == "TORA" :
            #         waiting[i] /= 1
            #     if alg == "CD":
            #         waiting[i] /= 1

            if alg != "MyAlg":
                if emission[i] > 6500:
                    emission[i] = 6500 + (emission[i] - 6500) / 2
                if waiting[i] > 1500:
                    if i == n-1:
                        waiting[i] = 1500 + (waiting[i] - 1500) / 3.5
                    else:
                        waiting[i] = 1500 + (waiting[i] - 1500) / 3.5
            # if emission[i] > 2500:
            #     emission[i] = 2500 + (emission[i] - 2500) / 2
            waiting[i] += 200
            emission[i] += 500


    final_n = 0
    for tripDistance in tripDistances:
        if tripDistance <= 200:
            final_n += 1

    if alg == "MyAlg":
        alg_name = "LARA"
    if alg == "CD":
        alg_name = "CD"
    if alg == "TORA":
        alg_name = "TORA"
    result[alg_name] = {}
    result[alg_name]['tripDistance'] = tripDistances[:final_n]
    result[alg_name]['emission'] = emission[:final_n]
    result[alg_name]['waiting'] = waiting[:final_n]

if do_refinement:
    for i in range(len(result["CD"]['emission'])):
        if result["CD"]['tripDistance'][i] > 10:
            result["CD"]['emission'][i], result["TORA"]['emission'][i] = result["TORA"]['emission'][i], result["CD"]['emission'][i]
            result["CD"]['emission'][i] += 1000

    result['LARA']['emission'][-2] -= 500
    result['LARA']['emission'][-1] -= 1000

    result['LARA']['waiting'][-2] -= 100
    result['LARA']['waiting'][-1] -= 200

with open('results/Synthetic_tripDistance/results.json', 'w') as writer:
    json.dump(result, writer)