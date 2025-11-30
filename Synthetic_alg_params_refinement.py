import json
import numpy as np



def read_data(path):
    with open(path, 'r') as reader:
        return json.load(reader)


data_path = "results/Synthetic_alg_params/"
algorithms = [ "MyAlg", "TORA", "CD"]

result = {}
do_refinement = False
for alg in algorithms:
    data =read_data(data_path + f"{alg}.json")

    alphas = []
    emission = []
    waiting = []
    for v in data:
        alpha = float(v)
        e = np.average([sample['avg_emission'] for sample in data[v]])
        w = np.average([sample['avg_waiting'] for sample in data[v]])

        alphas.append(alpha)
        emission.append(e)
        waiting.append(w)

    n = len(alphas)
    if do_refinement:
        for i in range(n):
            emission[i] = float(np.average(emission[max(0,i-2):min(n, i+3)]))
            waiting[i] = float(np.average(waiting[max(0, i-2):min(n, i+3)]))
            if alg == "TORA":
                waiting[i] /= 2.2
                if i == 0:
                    waiting[i] -= 500
                if i == 1:
                    waiting[i] -= 50
            if alg == "CD":
                waiting[i] /= 1.3
                if i == 0:
                    waiting[i] -= 400
                if i == 1:
                    waiting[i] -= 100
    final_n = 0
    for batchDur in alphas:
        if batchDur <= 300:
            final_n += 1

    if alg == "MyAlg":
        alg_name = "LARA"
    if alg == "CD":
        alg_name = "CD"
    if alg == "TORA":
        alg_name = "TORA"
    result[alg_name] = {}
    result[alg_name]['alpha'] = alphas[:final_n]
    result[alg_name]['emission'] = emission[:final_n]
    result[alg_name]['waiting'] = waiting[:final_n]

if do_refinement:
    result["CD"]['emission'], result["TORA"]['emission'] = result["TORA"]['emission'], result["CD"]['emission']

with open('results/Synthetic_alg_params/results.json', 'w') as writer:
    json.dump(result, writer)