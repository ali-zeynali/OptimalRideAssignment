from matplotlib import pyplot as plt
import json
import numpy as np
import mpltex
import matplotlib.font_manager as fm

path = "results/Understanding/"

def read_data(path):
    with open(path, 'r') as reader:
        return json.load(reader)

plt.rcParams["font.family"] = "Times New Roman"
plt.rcParams.update({'font.size': 14})
fig = plt.figure(0, figsize=(6, 3))
data =read_data(path + "d_vs_q.json")
# linestyles = mpltex.linestyle_generator()
linestyles = mpltex.linestyle_generator(colors=['tab:blue', 'tab:green', 'tab:red'],
                                        lines=['solid', 'dashed','dotted'],
                                        markers=['o','x', 's'],
                                        hollow_styles=[],)
deadhead_options = [1, 2, 5, 10, 15, 30]
x_max = 100
for alpha in data:
    n_samples = len(data[alpha]['n'])
    x = [data[alpha]['n'][0]]
    y = [data[alpha]['d'][0]]
    for i in range(1, n_samples):
        n = data[alpha]['n'][i]
        v = data[alpha]['d'][i]
        if n> x_max:
            break
        if v == y[-1]:
            x.append(n)
            y.append(v)
        else:
            x.append(n)
            y.append(y[-1])

            x.append(n)
            y.append(v)

    # plt.plot(x, y, label=fr"$\gamma =$ {gamma}")
    plt.plot(x, y, label=fr"$\alpha =$ {alpha}", linewidth=2.5, **next(linestyles), ms=5, markevery=10)

for i,d in enumerate(deadhead_options):
    if i == 0:
        plt.plot([0, x_max], [d, d], label='Deadhead limit options', linestyle='dashed', color="gray",
                 linewidth=0.7)
    else:
        plt.plot([0, x_max], [d, d], label='_nolegend_', linestyle='dashed', color="gray",
             linewidth=0.7)

# plt.legend()
# plt.legend(ncol=4, fontsize=14, loc='upper center', bbox_to_anchor=(0.5, 1.45))
plt.xlabel("Number of requests in the assignment queue", fontsize=16)
plt.ylabel("Selected deadhead limit (km)", fontsize=15)

ax = plt.gca()
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.spines['left'].set_linewidth(1.5)
ax.spines['bottom'].set_linewidth(1.5)
ax.xaxis.set_tick_params(width=1.5)
ax.yaxis.set_tick_params(width=1.5)

font_properties = fm.FontProperties(size=14)

# plt.legend()
# plt.savefig(path + "understanding_d_vs_q.png", dpi=400,  bbox_inches='tight')
plt.savefig(path + "understanding_d_vs_q.pdf", format="pdf",  bbox_inches='tight')

##########################################
fig = plt.figure(1, figsize=(6, 3))
data =read_data(path + "d_vs_Qmax.json")
# linestyles = mpltex.linestyle_generator()
linestyles = mpltex.linestyle_generator(colors=['tab:blue', 'tab:green', 'tab:red'],
                                        lines=['solid', 'dashed','dotted'],
                                        markers=['o','x', 's'],
                                        hollow_styles=[],)
deadhead_options = [1, 2, 5, 10, 15, 30]

for alpha in data:
    n_samples = len(data[alpha]['Q'])
    x = data[alpha]['Q']
    y = data[alpha]['d']

    # plt.plot(x, y, label=fr"$\gamma =$ {gamma}")
    plt.plot(x, y, label=fr"$\alpha =$ {alpha}", linewidth=2.5, **next(linestyles), ms=5, markevery=1)

for d in deadhead_options:
    plt.plot([10, 100], [d, d], label='_nolegend_', linestyle='dashed', color="gray",
             linewidth=0.7)

plt.xlabel(r"Q$_{\max}$", fontsize=16)
plt.ylabel("Selected deadhead limit (km)", fontsize=15)
# plt.xticks([5,10,15,20])
plt.xticks([20,40,60,80, 100])

plt.rc('font', family='serif', size=14)
ax = plt.gca()
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.spines['left'].set_linewidth(1.5)
ax.spines['bottom'].set_linewidth(1.5)
ax.xaxis.set_tick_params(width=1.5)
ax.yaxis.set_tick_params(width=1.5)

font_properties = fm.FontProperties(size=14)

# plt.legend()
# plt.savefig(path + "understanding_d_vs_Qmax.png", dpi=400,  bbox_inches='tight')
plt.savefig(path + "understanding_d_vs_Qmax.pdf", format="pdf",  bbox_inches='tight')