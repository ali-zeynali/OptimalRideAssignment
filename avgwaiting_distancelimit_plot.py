import json
import matplotlib.pyplot as plt

with open('results/all_distance_limits_results.json', 'r') as file:
    all_results = json.load(file)

distance_limits = []
avg_waitings = []

for key, value in all_results['total_info'].items():
    distance_limit = int(key.split('_')[-1])
    distance_limits.append(distance_limit)
    avg_waitings.append(value['avg_waiting'])

distance_limits, avg_waitings = zip(*sorted(zip(distance_limits, avg_waitings)))

plt.figure(figsize=(10, 6))
plt.plot(distance_limits, avg_waitings, label='Avg Waiting', marker='o')
plt.xlabel('Distance Limit (km)')
plt.ylabel('Avg Waiting Time (sec)')

plt.savefig('plots/avg_waiting_vs_distance_limits.pdf')
