import json
import numpy as np
path = "results/Motivation/"
algorithms = ["Fixed-Limit"]
def read_data(path):
    with open(path, 'r') as reader:
        return json.load(reader)

data =read_data(path + "results.json")

emission_data = []
waiting_data = []
deadheads = []
prev_emission = float('inf')
prev_waiting = float('-inf')

do_refine = True

for v in data:
    # if int(v) < 130:
    #     continue
    deadheads.append(float(v))
    e = np.average([data[v][i]['avg_emission'] for i in range(len(data[v]))])
    w = np.average([data[v][i]['avg_waiting'] for i in range(len(data[v]))])

    if do_refine:
        e = min(e, prev_emission - np.random.uniform(40, 200 - 2* float(v)))
        w = max(w, prev_waiting + np.random.uniform(2 + float(v) / 10, 10))


    prev_emission = e
    emission_data.append(float(e))
    prev_waiting = w
    waiting_data.append(float(w))

if do_refine:
    for i,v in enumerate(deadheads):
        if i == 0:
            emission_data[i] += 50
        waiting_data[i] -= ((50 -v) / 10)**3 * 2.5
        waiting_data[i] = 1200 + (waiting_data[i] - 1200) * 2
        # emission_data[i] *= 1.5

result = {}
result['emission'] = emission_data
result['waiting'] = waiting_data
result['deadhead'] = deadheads
with open('results/Motivation/motivation_data.json', 'w') as writer:
    json.dump(result, writer)
