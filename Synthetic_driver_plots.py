from matplotlib import pyplot as plt
import json

data_path = "results/Synthetic_drivers/"
path_to_save = "results/Synthetic_drivers_plots/"
algorithms = [ "MyAlg", "TORA", "Fixed-10", "Fixed-20", "Fixed-30"]
algorithms = [ "MyAlg", "TORA", "Fixed-10"]
def read_data(path):
    with open(path, 'r') as reader:
        return json.load(reader)

for alg in algorithms:
    data =read_data(data_path + f"{alg}.json")
    x = []
    y = []
    for v in data:
        if int(v) < 130:
            continue
        x.append(int(v))
        # y.append(data[v]['avg_emission'])
        y.append(data[v]['avg_waiting'])
    plt.plot(x, y, label=alg)

plt.xlabel("Number of drivers")
plt.ylabel("Avg. Emission")
plt.legend()
plt.savefig(path_to_save + "synthetic_emission_vs_driver.png", dpi=400,  bbox_inches='tight')