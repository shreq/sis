import matplotlib.pyplot as plt
import numpy as np
from gather_data import gather_data


bfs_dfs_data, astr_data = gather_data()
width = 0.3

# astar plots
for statistic in astr_data.keys():
    hamm_data = []
    manh_data = []
    for complexity in astr_data[statistic].keys():
        hamm_data.append(astr_data[statistic][complexity]['hamm'])
        manh_data.append(astr_data[statistic][complexity]['manh'])
    ind = np.arange(1, 8)
    plt.bar(ind - width/2, manh_data, width, label='manhattan')
    plt.bar(ind + width/2, hamm_data, width, label='hamming')
    plt.xlabel("Puzzle complexity")
    plt.minorticks_on()
    plt.grid(True, which="major", axis="y", ls="--", color="black")
    plt.grid(True, which="minor", axis="y", ls="--")
    plt.legend(title="Heuristics:")
    plt.yscale('linear')
    plt.ylabel(statistic)
    plt.title("A*: " + statistic)
    plt.show()


width = 0.1
priorities = bfs_dfs_data['bfs']['time']['01'].keys()

for algorithm in bfs_dfs_data.keys():
    for statistic in bfs_dfs_data[algorithm].keys():
        data_series = [[] for i in range(8)]
        for complexity in bfs_dfs_data[algorithm][statistic].keys():
            for c, priority in enumerate(bfs_dfs_data[algorithm][statistic][complexity].keys()):
                data_series[c].append(bfs_dfs_data[algorithm][statistic][complexity][priority])
        plt.rc('xtick', labelsize=15)
        plt.rc('ytick', labelsize=15)
        plt.rc('legend', fontsize=12)
        plt.rc('axes', titlesize=15)

        fig = plt.figure(figsize=(21, 10), dpi=75)
        ax1 = fig.add_subplot(111)
        bar_number = 8
        start_x = np.arange(1, 8) - (bar_number * width) / 2
        bar_x_tick = []
        bar_x_label = []
        for c, (data, priority) in enumerate(zip(data_series, priorities)):
            bar_pos = start_x + c * width
            bar_x_tick.extend(bar_pos)
            bar_x_label.extend([priority] * 7)
            ax1.bar(bar_pos,
                    data,
                    width,
                    align="edge",
                    label=priority)
        ax1.set_xlabel("Search priorities")
        ax1.grid(True)

        ax2 = ax1.twiny()
        ax2.set_xlabel("Puzzle complexity")
        ax1.set_ylabel(statistic)

        ax2.set_xticks(range(0, 8))
        ax2.set_xbound(ax1.get_xbound())
        ax1.set_xticks(bar_x_tick)

        ax1.set_xticklabels(bar_x_label, rotation='vertical')
        ax1.set_yscale('linear')
        ax1.legend(title="Priorities:")
        plt.title(algorithm + " " + statistic)
        plt.show()


