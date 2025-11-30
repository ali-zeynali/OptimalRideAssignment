from matplotlib import pyplot as plt
import json
import mpltex
import matplotlib.font_manager as fm

data_path = "results/Synthetic_tripDistance/"
path_to_save = "results/Synthetic_tripDistance_plots/"
algorithms = [ "MyAlg", "TORA", "CD"]

def read_data(path):
    with open(path, 'r') as reader:
        return json.load(reader)

plt.rcParams["font.family"] = "Times New Roman"
plt.rcParams.update({'font.size': 12})
linestyles = mpltex.linestyle_generator(colors=['black', 'tab:red', 'tab:green', 'tab:purple'],
                                        lines=['solid', 'dashed','dotted', 'dashdot'],
                                        markers=['o', 's','x', '*'],
                                        hollow_styles=[],)

data = read_data(data_path+ "results.json")
fig = plt.figure(0, figsize=(6, 3))

for alg in data:
    x = data[alg]['tripDistance']
    y = data[alg]['emission']
    plt.plot(x, y, **next(linestyles), linewidth=3, label=alg)

font_properties = fm.FontProperties(size=12)
plt.xlabel("Avg. Trip distance (km)", fontsize=16)
plt.ylabel("Avg. Emission of trips (gCO2)", fontsize=14)
# plt.legend()
plt.legend(loc='upper center', bbox_to_anchor=(0.6, 0.18), ncol=4, prop=font_properties)
ax = plt.gca()
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.spines['left'].set_linewidth(1.2)
ax.spines['bottom'].set_linewidth(1.2)
ax.xaxis.set_tick_params(width=1.2)
ax.yaxis.set_tick_params(width=1.2)
plt.yticks([0, 2000, 4000, 6000, 8000, 10000])


plt.savefig(path_to_save + "synthetic_emission_vs_tripDistance.png", dpi=400,  bbox_inches='tight')
plt.savefig(path_to_save + "synthetic_emission_vs_tripDistance.pdf", format="pdf",  bbox_inches='tight')
########################################
linestyles = mpltex.linestyle_generator(colors=['black', 'tab:red', 'tab:green', 'tab:purple'],
                                        lines=['solid', 'dashed','dotted', 'dashdot'],
                                        markers=['o', 's','x', '*'],
                                        hollow_styles=[],)

fig = plt.figure(1, figsize=(6, 3))
for alg in data:
    x = data[alg]['tripDistance']
    y = data[alg]['waiting']
    plt.plot(x, y, **next(linestyles), linewidth=3, label=alg)


plt.xlabel("Avg. Trip distance (km)", fontsize=16)
plt.ylabel("Avg. Waiting times (s)", fontsize=16)
# plt.legend()
plt.legend(loc='upper center', bbox_to_anchor=(0.6, 0.18), ncol=4, prop=font_properties)
ax = plt.gca()
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.spines['left'].set_linewidth(1.2)
ax.spines['bottom'].set_linewidth(1.2)
ax.xaxis.set_tick_params(width=1.2)
ax.yaxis.set_tick_params(width=1.2)
plt.yticks([0, 1000, 2000, 3000, 4000])
font_properties = fm.FontProperties(size=12)
plt.savefig(path_to_save + "synthetic_waiting_vs_tripDistance.png", dpi=400,  bbox_inches='tight')
plt.savefig(path_to_save + "synthetic_waiting_vs_tripDistance.pdf", format="pdf",  bbox_inches='tight')


# plt.figure(2)
# for alg in algorithms:
#     data =read_data(data_path + f"{alg}.json")
#     x = []
#     y = []
#     for v in data:
#         # if int(v) < 130:
#         #     continue
#         x.append(int(v))
#         y.append(data[v]['n_unassignment'])
#     plt.plot(x, y, label=alg)
#
# plt.xlabel("Avg. Trip Distance")
# plt.ylabel("Number of un-assigned requests")
# plt.legend()
# plt.savefig(path_to_save + "synthetic_unassigned_vs_tripDistance.png", dpi=400,  bbox_inches='tight')