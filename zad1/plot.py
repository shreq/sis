import os
import matplotlib.pyplot as plt
import numpy as np
from gather_data import gather_data
from unicodedata import normalize

if not os.path.exists('charts'):
    os.makedirs('charts')

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
    plt.xlabel("skomplikowanie puzzli")
    plt.minorticks_on()
    plt.grid(True, which="major", axis="y", ls="--", color="black")
    plt.grid(True, which="minor", axis="y", ls="--")
    plt.legend(title="Heurystyka:")
    plt.yscale('linear')
    plt.ylabel(statistic)
    plt.title("A*: " + statistic)
    plt.savefig("charts/astr_" + normalize('NFKD', statistic.replace('ł', 'l')).encode('ascii', 'ignore').decode('ascii'))
    # plt.show()
    plt.clf()


# bfs and dfs plots
width = 0.1
priorities = bfs_dfs_data['bfs']['czas [ms]']['01'].keys()

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
        ax1.set_xlabel("priorytety")
        ax1.grid(True)

        ax2 = ax1.twiny()
        ax2.set_xlabel("skomplikowanie puzzli")
        ax1.set_ylabel(statistic)

        ax2.set_xticks(range(0, 8))
        ax2.set_xbound(ax1.get_xbound())
        ax1.set_xticks(bar_x_tick)

        ax1.set_xticklabels(bar_x_label, rotation='vertical')
        if statistic == 'stany przetworzone' or statistic == 'stany odwiedzone' or (statistic == 'czas [ms]'):
            ax1.set_yscale('log')
        else:
            ax1.set_yscale('linear')
        ax1.legend(title="Priorytety:")
        plt.title(algorithm + " " + statistic)
        plt.savefig("charts/" + algorithm + '_' + normalize('NFKD', statistic.replace('ł', 'l')).encode('ascii', 'ignore').decode('ascii'))
        # plt.show()
        plt.clf()


# combined plots
width = 0.25
bfs_data = bfs_dfs_data['bfs']
dfs_data = bfs_dfs_data['dfs']

for statistic in astr_data.keys():
    astr_avg = [0] * 7
    bfs_avg = [0] * 7
    dfs_avg = [0] * 7
    for name, algorithm in zip(['astr', 'bfs', 'dfs'], [astr_data, bfs_data, dfs_data]):
        for index, complexity in enumerate(algorithm[statistic].keys()):
            for priority in algorithm[statistic][complexity].keys():
                if name == 'astr':
                    astr_avg[index] += algorithm[statistic][complexity][priority] / 2
                elif name == 'bfs':
                    bfs_avg[index] += algorithm[statistic][complexity][priority] / 8
                else:
                    dfs_avg[index] += algorithm[statistic][complexity][priority] / 8

    pos = np.arange(1, 8)
    plt.bar(pos - (width * 1.5), astr_avg, width, label="A*", align="edge")
    plt.bar(pos, bfs_avg, width, label="BFS")
    plt.bar(pos + width * 0.5, dfs_avg, width, label="DFS", align="edge")
    plt.minorticks_on()
    plt.grid(True, which="major", axis="y", ls="--", color="black")
    plt.legend(title="Algorytm: ")
    plt.xlabel("skomplikowanie puzzli")
    plt.ylabel(statistic)
    plt.title("Porównanie algorytmów: " + statistic)
    if statistic == 'stany przetworzone' or statistic == 'stany odwiedzone' or statistic == 'czas [ms]':
        plt.yscale('log')
    else:
        plt.yscale('linear')
    plt.savefig("charts/all_" + normalize('NFKD', statistic.replace('ł', 'l')).encode('ascii', 'ignore').decode('ascii'))
    # plt.show()
    plt.clf()
