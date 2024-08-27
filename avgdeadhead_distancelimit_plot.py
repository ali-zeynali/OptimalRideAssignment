import json
import matplotlib.pyplot as plt

with open('results/all_distance_limits_results.json', 'r') as file:
    all_results = json.load(file)

distance_limits = []
avg_deadheads = []

for key, value in all_results['total_info'].items():
    distance_limit = int(key.split('_')[-1])
    distance_limits.append(distance_limit)
    avg_deadheads.append(value['avg_deadhead'])

distance_limits, avg_deadheads = zip(*sorted(zip(distance_limits, avg_deadheads)))

plt.figure(figsize=(10, 6))
plt.plot(distance_limits, avg_deadheads, label='Avg Deadhead', marker='o')
# plt.plot(distance_limits, distance_limits, label="X=Y")
plt.xlabel('Distance Limit (km)')
plt.ylabel('Avg Deadhead (km)')
# plt.legend()
plt.savefig('plots/avg_deadhead_vs_distance_limits.pdf')
