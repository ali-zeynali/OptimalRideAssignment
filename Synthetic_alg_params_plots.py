from matplotlib import pyplot as plt
import json
import mpltex
import matplotlib.font_manager as fm


data_path = "results/Synthetic_alg_params/"
path_to_save = "results/Synthetic_alg_paramsـ_plots/"
# algorithms = [ "MyAlg", "TORA", "CD" ,"Fixed-10", "Fixed-20", "Fixed-30"]
# algorithms = [ "MyAlg", "TORA", "CD"]

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
    x = data["LARA"]['alpha']
    if alg == "LARA":
        y = data[alg]['emission']
    else:
        y = [data[alg]['emission'][0] for v in x]
    plt.plot(x, y, **next(linestyles), linewidth=3, label=alg)

font_properties = fm.FontProperties(size=12)
# plt.yticks([5500, 6500, 7500, 8500])
plt.xlabel(r"$\alpha$", fontsize=16)
plt.ylabel("Avg. Emission of trips (gCO2)", fontsize=14)
# plt.legend()
plt.legend(loc='upper center', bbox_to_anchor=(0.44, 1.1), ncol=4, prop=font_properties)
ax = plt.gca()
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.spines['left'].set_linewidth(1.2)
ax.spines['bottom'].set_linewidth(1.2)
ax.xaxis.set_tick_params(width=1.2)
ax.yaxis.set_tick_params(width=1.2)



plt.savefig(path_to_save + "synthetic_emission_vs_alpha.png", dpi=400,  bbox_inches='tight')
# plt.savefig(path_to_save + "synthetic_emission_vs_alpha.pdf", format="pdf",  bbox_inches='tight')

######################################
linestyles = mpltex.linestyle_generator(colors=['black', 'tab:red', 'tab:green', 'tab:purple'],
                                        lines=['solid', 'dashed','dotted', 'dashdot'],
                                        markers=['o', 's','x', '*'],
                                        hollow_styles=[],)

fig = plt.figure(1, figsize=(6, 3))
for alg in data:
    x = data["LARA"]['alpha']
    if alg == "LARA":
        y = data[alg]['waiting']
    else:
        y = [data[alg]['waiting'][0] for v in x]
    plt.plot(x, y, **next(linestyles), linewidth=3, label=alg)


plt.xlabel(r"$\alpha$", fontsize=16)
plt.ylabel("Avg. Waiting times (s)", fontsize=16)
# plt.legend()
plt.legend(loc='upper center', bbox_to_anchor=(0.44, 1.1), ncol=4, prop=font_properties)
ax = plt.gca()
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.spines['left'].set_linewidth(1.2)
ax.spines['bottom'].set_linewidth(1.2)
ax.xaxis.set_tick_params(width=1.2)
ax.yaxis.set_tick_params(width=1.2)

font_properties = fm.FontProperties(size=12)

plt.savefig(path_to_save + "synthetic_waiting_vs_alpha.png", dpi=400,  bbox_inches='tight')
# plt.savefig(path_to_save + "synthetic_waiting_vs_alpha.pdf", format="pdf",  bbox_inches='tight')


# plt.figure(2)
# for alg in algorithms:
#     data =read_data(data_path + f"{alg}.json")
#     x = []
#     y = []
#     for v in data:
#         # if int(v) < 130:
#         #     continue
#         x.append(int(v))
#         # y.append(data[v]['n_unassignment'])
#         y.append(np.average([sample['n_unassignment'] for sample in data[v]]))
#     plt.plot(x, y, label=alg)
#
# plt.xlabel("Batch Duration")
# plt.ylabel("Number of un-assigned requests")
# plt.legend()
# plt.savefig(path_to_save + "synthetic_unassigned_vs_batchDur.png", dpi=400,  bbox_inches='tight')