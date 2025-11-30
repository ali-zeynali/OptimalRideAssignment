from matplotlib import pyplot as plt
import json
import mpltex
import matplotlib.font_manager as fm
import mpl_toolkits.axes_grid1.inset_locator as il
import matplotlib.patches as patches

data_path = "results/Dataset_batchDuration/"
path_to_save = "results/Dataset_batchDuration_plots/"


def read_data(path):
    with open(path, 'r') as reader:
        return json.load(reader)


plt.rcParams["font.family"] = "Times New Roman"
plt.rcParams.update({'font.size': 12})

linestyles = mpltex.linestyle_generator(colors=['black', 'black', 'black', 'tab:red', 'tab:green', 'tab:purple'],
                                        lines=['solid', 'dashdot', 'dotted', 'dashed', 'dotted', 'dashdot'],
                                        markers=['o', 'v', 'p', 's', 'x', '*'],
                                        hollow_styles=[], )

algs = ["LARA-0.75", "LARA-0.50", "LARA-0.25", "TORA", "CD"]
data = read_data(data_path + "results.json")


def plot_with_inset(x_vals, y_vals, xlabel, ylabel, filename, yticks_main, xticks_main, zoom_xlim, zoom_ylim,
                    zoom_yticks, inset_corners):
    fig, ax = plt.subplots(figsize=(6, 3))

    linestyles = mpltex.linestyle_generator(colors=['black', 'black', 'black', 'tab:red', 'tab:green', 'tab:purple'],
                                            lines=['solid', 'dashdot', 'dotted', 'dashed', 'dotted', 'dashdot'],
                                            markers=['o', 'v', 'p', 's', 'x', '*'],
                                            hollow_styles=[], )

    for alg in algs:
        ax.plot(x_vals[alg], y_vals[alg], **next(linestyles), linewidth=3, label=alg)

    ax.set_xlabel(xlabel, fontsize=16)
    ax.set_ylabel(ylabel, fontsize=14)
    ax.set_yticks(yticks_main)

    # Removing top and right spines
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_linewidth(1.2)
    ax.spines['bottom'].set_linewidth(1.2)
    ax.xaxis.set_tick_params(width=1.2)
    ax.yaxis.set_tick_params(width=1.2)

    # Create an inset
    ax_inset = il.inset_axes(ax, width="100%", height="100%", bbox_to_anchor=(0.15, 0.15, 0.85, 0.4),
                             bbox_transform=ax.transAxes)

    linestyles = mpltex.linestyle_generator(colors=['black', 'black', 'black', 'tab:red', 'tab:green', 'tab:purple'],
                                            lines=['solid', 'dashdot', 'dotted', 'dashed', 'dotted', 'dashdot'],
                                            markers=['o', 'v', 'p', 's', 'x', '*'],
                                            hollow_styles=[], )

    for alg in algs:
        ax_inset.plot(x_vals[alg], y_vals[alg], **next(linestyles), linewidth=2)

    ax_inset.set_xlim(zoom_xlim)
    ax_inset.set_ylim(zoom_ylim)
    ax_inset.set_yticks(zoom_yticks)
    ax_inset.tick_params(labelsize=9)

    # Highlight zoomed area
    ax.add_patch(
        patches.Rectangle((zoom_xlim[0], zoom_ylim[0]), zoom_xlim[1] - zoom_xlim[0], zoom_ylim[1] - zoom_ylim[0],
                          linewidth=1, edgecolor="k", facecolor="lightgrey", alpha=0.5, zorder=-99))

    # Draw connection lines from main plot to inset
    rect_corners = [
        (zoom_xlim[0], zoom_ylim[0]),  # Lower left of the gray area in the main plot
        (zoom_xlim[1], zoom_ylim[0])  # Lower right of the gray area in the main plot
    ]

    # inset_corners = [
    #     ax_inset.transData.inverted().transform(ax.transData.transform((zoom_xlim[0], zoom_ylim[0]))),
    #     # Top left in inset
    #     ax_inset.transData.inverted().transform(ax.transData.transform((zoom_xlim[1], zoom_ylim[0])))
    #     # Top right in inset
    # ]

    #
    for (x_main, y_main), (x_inset, y_inset) in zip(rect_corners, inset_corners):
        ax.plot([x_main, x_inset], [y_main, y_inset], "k--", linewidth=1, alpha=0.5)
    #
    ax.set_yticks(yticks_main)
    ax.set_xticks(xticks_main[:-1])
    ax.set_xlim((xticks_main[0], xticks_main[-1]))

    plt.savefig(path_to_save + filename + ".png", dpi=400, bbox_inches='tight')
    plt.savefig(path_to_save + filename + ".pdf", format="pdf", bbox_inches='tight')


# First plot: Emission vs Batch Duration
plot_with_inset(
    x_vals={alg: data[alg]['batchDur'] for alg in algs},
    y_vals={alg: data[alg]['emission'] for alg in algs},
    xlabel="Batch duration (s)",
    ylabel="Avg. Emission of trips (gCO2)",
    filename="dataset_emission_vs_batchDur_zoom",
    yticks_main=[0, 1000, 2000, 3000],
    xticks_main=[50, 100, 150, 200, 250, 300, 320],
    zoom_xlim=(50, 320),  # Adjusted zoomed-in x range
    zoom_ylim=(2400, 3250),  # Adjusted zoomed-in y range
    zoom_yticks=[2600, 2800, 3000],
    inset_corners=[
        (86, 1700),
        (315, 1700)
    ]
)

# Second plot: Waiting time vs Batch Duration
plot_with_inset(
    x_vals={alg: data[alg]['batchDur'] for alg in algs},
    y_vals={alg: data[alg]['waiting'] for alg in algs},
    xlabel="Batch duration (s)",
    ylabel="Avg. Waiting times (s)",
    filename="dataset_waiting_vs_batchDur_zoom",
    yticks_main=[0, 600, 1200, 1800],
    xticks_main=[50, 100, 150, 200, 250, 300, 320],
    zoom_xlim=(50, 320),  # Adjusted zoomed-in x range
    zoom_ylim=(1200, 1950),  # Adjusted zoomed-in y range
    zoom_yticks=[1400, 1600, 1800],
    inset_corners=[
        (86, 1022),
        (315, 1022)
    ]
)

#
