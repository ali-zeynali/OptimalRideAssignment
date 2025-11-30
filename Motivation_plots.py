from matplotlib import pyplot as plt
import json
import numpy as np
import mpltex
import matplotlib.font_manager as fm

path = "results/Motivation/"
algorithms = ["Fixed-Limit"]
def read_data(path):
    with open(path, 'r') as reader:
        return json.load(reader)

plt.rcParams["font.family"] = "Times New Roman"
plt.rcParams.update({'font.size': 14})
linestyles = mpltex.linestyle_generator(colors=['black', 'black', 'black', 'black'],
                                        lines=['solid','dotted', 'dashed', 'dashdot'],
                                        markers=['o','x', 's', '*'],
                                        hollow_styles=[],)

fig = plt.figure(0, figsize=(6, 3))
for alg in algorithms:
    data =read_data(path + "motivation_data.json")
    x = data['deadhead']
    y = data['emission']
    # for v in data:
    #     # if int(v) < 130:
    #     #     continue
    #     x.append(int(v))
    #     y.append(np.average([data[v][i]['avg_emission'] for i in range(len(data[v]))]))
        # y.append(np.average([data[v][i]['alg_closest_emission'] for i in range(len(data[v]))]) - np.average([data[v][i]['alg_emission_reduction'] for i in range(len(data[v]))]))
    # plt.plot(x, y, label=alg)
    plt.plot(x,y,**next(linestyles),linewidth=3)



plt.xlabel("Limit on deadhead distances (km)", fontsize=16)
plt.ylabel("Avg. Emission of trips (gCO2)", fontsize=14)

ax = plt.gca()
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.spines['left'].set_linewidth(1.2)
ax.spines['bottom'].set_linewidth(1.2)
ax.xaxis.set_tick_params(width=1.2)
ax.yaxis.set_tick_params(width=1.2)
# plt.yticks([0 , 2000, 4000, 6000])
font_properties = fm.FontProperties(size=12)
# plt.legend(loc='upper center', bbox_to_anchor=(0.74, 1.2), ncol=1, prop=font_properties)
plt.legend('',frameon=False)

# plt.xticks([2, 5, 10, 15], fontsize=14)
# plt.yticks([300, 350, 400, 450, 500, 550, 600], fontsize=14)


# plt.legend()
plt.savefig(path + "motivation_emission.pdf", format="pdf",  bbox_inches='tight')
plt.savefig(path + "motivation_emission.png",dpi=400,  bbox_inches='tight')
########################
linestyles = mpltex.linestyle_generator(colors=['black', 'black', 'black', 'black'],
                                        lines=['solid','dotted', 'dashed', 'dashdot'],
                                        markers=['o','x', 's', '*'],
                                        hollow_styles=[],)

fig = plt.figure(1, figsize=(6, 3))
for alg in algorithms:
    data =read_data(path + "motivation_data.json")
    x = data['deadhead']
    y = data['waiting']
    # for v in data:
    #     # if int(v) < 130:
    #     #     continue
    #     x.append(int(v))
    #     y.append(np.average([data[v][i]['avg_emission'] for i in range(len(data[v]))]))
        # y.append(np.average([data[v][i]['alg_closest_emission'] for i in range(len(data[v]))]) - np.average([data[v][i]['alg_emission_reduction'] for i in range(len(data[v]))]))
    # plt.plot(x, y, label=alg)
    plt.plot(x,y,**next(linestyles),linewidth=3)



plt.xlabel("Limit on deadhead distances (km)", fontsize=16)
plt.ylabel("Avg. Waiting times (s)", fontsize=16)

ax = plt.gca()
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.spines['left'].set_linewidth(1.2)
ax.spines['bottom'].set_linewidth(1.2)
ax.xaxis.set_tick_params(width=1.2)
ax.yaxis.set_tick_params(width=1.2)
# plt.yticks([0, 500 ,1000, 1500, 2000])
font_properties = fm.FontProperties(size=12)
# plt.legend(loc='upper center', bbox_to_anchor=(0.74, 1.2), ncol=1, prop=font_properties)
plt.legend('',frameon=False)

# plt.xticks([2, 5, 10, 15], fontsize=14)
# plt.yticks([1200, 1400, 1450 ,1500, 1550], fontsize=14)


# plt.legend()
plt.savefig(path + "motivation_waiting.pdf", format="pdf",  bbox_inches='tight')
plt.savefig(path + "motivation_waiting.png",dpi=400,  bbox_inches='tight')

#####

