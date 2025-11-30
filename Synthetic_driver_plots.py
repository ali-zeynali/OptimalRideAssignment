from matplotlib import pyplot as plt
import json
import numpy as np
import mpltex
import matplotlib.font_manager as fm

data_path = "results/Synthetic_drivers/"
path_to_save = "results/Synthetic_drivers_plots/"
algorithms = [ "MyAlg", "TORA", "Fixed-10", "Fixed-20", "Fixed-30", "CD"]
algorithms = [ "MyAlg", "TORA",  "CD"]

linestyles = mpltex.linestyle_generator(colors=['black', 'tab:red', 'tab:green', 'tab:purple'],
                                        lines=['solid', 'dashed','dotted', 'dashdot'],
                                        markers=['o', 's','x', '*'],
                                        hollow_styles=[],)

plt.rcParams["font.family"] = "Times New Roman"
plt.rcParams.update({'font.size': 12})
def read_data(path):
    with open(path, 'r') as reader:
        return json.load(reader)

fig = plt.figure(0, figsize=(6, 3))

data = read_data(data_path+ "results.json")
for alg in data:
    x = data[alg]['drivers']
    y = data[alg]['emission']
    # data =read_data(data_path + f"{alg}.json")
    # x = []
    # y = []
    # for v in data:
    #     # if int(v) < 130:
    #     #     continue
    #     x.append(int(v))
    #     y.append(np.average([sample['avg_emission'] for sample in data[v]]))
    plt.plot(x, y, **next(linestyles), linewidth=3, label=alg)

font_properties = fm.FontProperties(size=12)
plt.xlabel("Number of drivers", fontsize=16)
plt.ylabel("Avg. Emission of trips (gCO2)", fontsize=14)
# plt.legend()
plt.legend(loc='upper center', bbox_to_anchor=(0.44, 0.2), ncol=4, prop=font_properties)
ax = plt.gca()
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.spines['left'].set_linewidth(1.2)
ax.spines['bottom'].set_linewidth(1.2)
ax.xaxis.set_tick_params(width=1.2)
ax.yaxis.set_tick_params(width=1.2)


plt.yticks([0, 2000, 4000 ,6000, 8000])
plt.xticks([300, 350, 400, 450,500])
plt.savefig(path_to_save + "synthetic_emission_vs_driver.png", dpi=400,  bbox_inches='tight')
plt.savefig(path_to_save + "synthetic_emission_vs_driver.pdf", format="pdf",  bbox_inches='tight')
#######################################
linestyles = mpltex.linestyle_generator(colors=['black', 'tab:red', 'tab:green', 'tab:purple'],
                                        lines=['solid', 'dashed','dotted', 'dashdot'],
                                        markers=['o', 's','x', '*'],
                                        hollow_styles=[],)

fig = plt.figure(1, figsize=(6, 3))
for alg in data:
    x = data[alg]['drivers']
    y = data[alg]['waiting']
    # data =read_data(data_path + f"{alg}.json")
    # x = []
    # y = []
    # for v in data:
    #     # if int(v) < 130:
    #     #     continue
    #     x.append(int(v))
    #     y.append(np.average([sample['avg_waiting'] for sample in data[v]]))
    plt.plot(x, y, **next(linestyles), linewidth=3, label=alg)

plt.xlabel("Number of drivers", fontsize=16)
plt.ylabel("Avg. Waiting times (s)", fontsize=16)
# plt.legend()
plt.legend(loc='upper center', bbox_to_anchor=(0.44, 0.2), ncol=4, prop=font_properties)
ax = plt.gca()
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.spines['left'].set_linewidth(1.2)
ax.spines['bottom'].set_linewidth(1.2)
ax.xaxis.set_tick_params(width=1.2)
ax.yaxis.set_tick_params(width=1.2)
plt.yticks([0, 1000, 2000, 3000, 4000])
plt.xticks([300, 350, 400, 450,500])
font_properties = fm.FontProperties(size=12)
plt.savefig(path_to_save + "synthetic_waiting_vs_driver.png", dpi=400,  bbox_inches='tight')
plt.savefig(path_to_save + "synthetic_waiting_vs_driver.pdf", format="pdf",  bbox_inches='tight')

#
# plt.figure(2)
# for alg in algorithms:
#     data =read_data(data_path + f"{alg}.json")
#     x = []
#     y = []
#     for v in data:
#         # if int(v) < 130:
#         #     continue
#         x.append(int(v))
#         y.append(np.average([sample['n_unassignment'] for sample in data[v]]))
#     plt.plot(x, y, label=alg)
#
# plt.xlabel("Number of drivers")
# plt.ylabel("Number of un-assigned requests")
# plt.legend()
# plt.savefig(path_to_save + "synthetic_unassigned_vs_driver.png", dpi=400,  bbox_inches='tight')