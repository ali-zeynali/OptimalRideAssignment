from matplotlib import pyplot as plt
import json
import mpltex
import matplotlib.font_manager as fm


data_path = "results/Dataset_batchDuration/"
path_to_save = "results/Dataset_batchDuration_plots/"
# algorithms = [ "MyAlg", "TORA", "CD" ,"Fixed-10", "Fixed-20", "Fixed-30"]
# algorithms = [ "MyAlg", "TORA", "CD"]

dataset_type = "_Texas"
# dataset_type = ""

def read_data(path):
    with open(path, 'r') as reader:
        return json.load(reader)

plt.rcParams["font.family"] = "Times New Roman"
plt.rcParams.update({'font.size': 12})
linestyles = mpltex.linestyle_generator(colors=['black','black','black', 'tab:red', 'tab:green', 'tab:purple'],
                                        lines=['solid','dashdot','dotted', 'dashed','dotted', 'dashdot'],
                                        markers=['o','v', 'p', 's','x', '*'],
                                        hollow_styles=[],)
algs = ["LARA-0.75", "LARA-0.50", "LARA-0.25", "TORA", "CD"]
data = read_data(data_path+ f"results{dataset_type}.json")
fig = plt.figure(0, figsize=(6, 3))
for alg in algs:
    x = data[alg]['batchDur']
    y = data[alg]['emission']
    plt.plot(x, y, **next(linestyles), linewidth=3, label=alg)

# plt.yticks([0, 1000, 2000, 3000])
font_properties = fm.FontProperties(size=10)
plt.xlabel("Batch duration (s)", fontsize=16)
plt.ylabel("Avg. Emission of trips (gCO2)", fontsize=14)
# plt.legend()
# plt.legend(loc='upper center', bbox_to_anchor=(0.44, 1.2), ncol=5, prop=font_properties)
ax = plt.gca()
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.spines['left'].set_linewidth(1.2)
ax.spines['bottom'].set_linewidth(1.2)
ax.xaxis.set_tick_params(width=1.2)
ax.yaxis.set_tick_params(width=1.2)



plt.savefig(path_to_save + f"dataset{dataset_type}_emission_vs_batchDur.png", dpi=400,  bbox_inches='tight')
plt.savefig(path_to_save + f"dataset{dataset_type}_emission_vs_batchDur.pdf", format="pdf",  bbox_inches='tight')

######################################
linestyles = mpltex.linestyle_generator(colors=['black','black','black', 'tab:red', 'tab:green', 'tab:purple'],
                                        lines=['solid','dashdot','dotted', 'dashed','dotted', 'dashdot'],
                                        markers=['o','v', 'p', 's','x', '*'],
                                        hollow_styles=[],)

fig = plt.figure(1, figsize=(6, 3))
for alg in algs:
    x = data[alg]['batchDur']
    y = data[alg]['waiting']
    plt.plot(x, y, **next(linestyles), linewidth=3, label=alg)


plt.xlabel("Batch duration (s)", fontsize=16)
plt.ylabel("Avg. Waiting times (s)", fontsize=16)
# plt.legend()
# plt.legend(loc='upper center', bbox_to_anchor=(0.44, 1.1), ncol=5, prop=font_properties)
ax = plt.gca()
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.spines['left'].set_linewidth(1.2)
ax.spines['bottom'].set_linewidth(1.2)
ax.xaxis.set_tick_params(width=1.2)
ax.yaxis.set_tick_params(width=1.2)
plt.yticks([0, 600, 1200, 1800])
font_properties = fm.FontProperties(size=12)

plt.savefig(path_to_save + f"dataset{dataset_type}_waiting_vs_batchDur.png", dpi=400,  bbox_inches='tight')
plt.savefig(path_to_save + f"dataset{dataset_type}_waiting_vs_batchDur.pdf", format="pdf",  bbox_inches='tight')

