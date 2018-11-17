import matplotlib.pyplot as plt
import numpy as np
from gather_data import gather_data


bfs_dfs_data, astr_data = gather_data()
width = 0.3

for statistic in astr_data.keys():
    hamm_data = []
    manh_data = []
    for complexity in astr_data[statistic].keys():
        hamm_data.append(astr_data[statistic][complexity]['hamm'])
        manh_data.append(astr_data[statistic][complexity]['manh'])
    ind = np.arange(7)
    plt.bar(ind - width/2, manh_data, width, label = 'manhattan')
    plt.bar(ind + width/2, hamm_data, width, label = 'hamming')
    plt.xlabel("Złożoność układanki")
    plt.minorticks_on()
    plt.grid(True, which="major", axis="y", ls="--", color="black")
    plt.grid(True, which="minor", axis="y", ls="--")
    plt.legend(title="Metryki:")
    plt.yscale('log')
    plt.ylabel(statistic)
    plt.title("A*:" + statistic)
    plt.show()

