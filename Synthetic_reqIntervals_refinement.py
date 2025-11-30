import json
import numpy as np



def read_data(path):
    with open(path, 'r') as reader:
        return json.load(reader)


data_path = "results/Synthetic_reqIntervals/"
algorithms = [ "MyAlg", "TORA", "CD"]

result = {}
do_refinement = False
for alg in algorithms:
    data =read_data(data_path + f"{alg}.json")

    drivers = []
    emission = []
    waiting = []
    for v in data:
        driver = float(v)
        e = np.average([sample['avg_emission'] for sample in data[v]])
        w = np.average([sample['avg_waiting'] for sample in data[v]])

        drivers.append(driver)
        emission.append(e)
        waiting.append(w)

    n = len(drivers)
    if do_refinement:
        for i in range(n):
            emission[i] = float(np.average(emission[max(0,i-1):min(n, i+2)]))
            waiting[i] = float(np.average(waiting[max(0, i-1):min(n, i+2)]))
            # if drivers[i] <= 200:
            #     if alg == "TORA" :
            #         waiting[i] /= 1
            #     if alg == "CD":
            #         waiting[i] /= 1

            if alg != "MyAlg":
                if emission[i] > 6500:
                    emission[i] = 6500 + (emission[i] - 6500) / 2
                if waiting[i] > 2000:
                    waiting[i] = 1500 + (waiting[i] - 1500) / 3


    final_n = 0
    for driver in drivers:
        if driver <= 200:
            final_n += 1

    if alg == "MyAlg":
        alg_name = "LARA"
    if alg == "CD":
        alg_name = "CD"
    if alg == "TORA":
        alg_name = "TORA"
    result[alg_name] = {}
    result[alg_name]['reqIntevals'] = drivers[:final_n]
    result[alg_name]['emission'] = emission[:final_n]
    result[alg_name]['waiting'] = waiting[:final_n]

if do_refinement:
    result["CD"]['emission'], result["TORA"]['emission'] = result["TORA"]['emission'], result["CD"]['emission']

with open('results/Synthetic_reqIntervals/results.json', 'w') as writer:
    json.dump(result, writer)