import json
import matplotlib.pyplot as plt

with open('results/all_distance_limits_results.json', 'r') as file:
    all_results = json.load(file)

distance_limits = []
avg_emissions = []

for key, value in all_results['total_info'].items():
    distance_limit = int(key.split('_')[-1])
    distance_limits.append(distance_limit)
    avg_emissions.append(value['avg_emission'])

distance_limits, avg_emissions = zip(*sorted(zip(distance_limits, avg_emissions)))

plt.figure(figsize=(10, 6))
plt.plot(distance_limits, avg_emissions, label='Avg Emission', marker='o')
plt.xlabel('Distance Limit (km)')
plt.ylabel('Avg Emission (gCO2)')

plt.savefig('plots/avg_emission_vs_distance_limits.pdf')
