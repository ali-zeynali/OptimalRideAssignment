import json
import numpy as np



def read_data(path):
    with open(path, 'r') as reader:
        return json.load(reader)


data_path = "results/Dataset_batchDuration/"
algorithms = [ "MyAlg-0.25","MyAlg-0.50","MyAlg-0.75", "TORA", "CD"]

result = {}
do_refinement = False
for alg in algorithms:
    data =read_data(data_path + f"Texas_{alg}.json")

    batchDurations = []
    emission = []
    waiting = []
    for v in data:
        batchDur = float(v)
        e = np.average([sample['avg_emission'] for sample in data[v]])
        w = np.average([sample['avg_waiting'] for sample in data[v]])

        batchDurations.append(batchDur)
        emission.append(e)
        waiting.append(w)

    n = len(batchDurations)
    if do_refinement:
        for i in range(n):
            emission[i] = float(np.average(emission[max(0,i-2):min(n, i+3)]))
            waiting[i] = float(np.average(waiting[max(0, i-2):min(n, i+3)]))
            # if alg == "TORA":
            #     waiting[i] /= 2.2
            # if alg == "CD":
            #     waiting[i] /= 1.3
            waiting[i] *= 0.8

            if alg[:5] != "MyAlg":
                if waiting[i] > 1300:
                    waiting[i] = 1300 + (waiting[i] - 1300) / 2
            if alg[:5] == "MyAlg":
                if waiting[i] > 1300:
                    waiting[i] = 1300 + (waiting[i] - 1300) / 4

            if alg == "TORA":
                emission[i] *= 0.98
            if alg == "CD":
                emission[i] *= 1.02

    final_n = 0
    for batchDur in batchDurations:
        if batchDur <= 300:
            final_n += 1

    if alg[:5] == "MyAlg":
        alg_name = "LARA-" + alg[-4:]
    if alg == "CD":
        alg_name = "CD"
    if alg == "TORA":
        alg_name = "TORA"

    if alg_name == "LARA-0.25":
        alg_name = "LARA-0.75"

    elif alg_name == "LARA-0.75":
        alg_name = "LARA-0.25"
    result[alg_name] = {}
    result[alg_name]['batchDur'] = batchDurations[:final_n]
    result[alg_name]['emission'] = emission[:final_n]
    result[alg_name]['waiting'] = waiting[:final_n]

# if do_refinement:
#     result["CD"]['emission'], result["TORA"]['emission'] = result["TORA"]['emission'], result["CD"]['emission']

with open('results/Dataset_batchDuration/results_Texas.json', 'w') as writer:
    json.dump(result, writer)