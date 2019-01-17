import os
import matplotlib.pyplot as plt
import numpy as np
from unicodedata import normalize


def gather_data():
    directory = os.fsencode('./output/')

    acceptable_error = [0.1, 0.01]
    learning_rate = [0.001, 0.0001]
    momentum = [0.001, 0.0001]
    hidden_size = [1, 2, 3, 4, 5]
    bias_switch = [0, 1]
    set_size = [25, 50]

    data = {}
    for stat in ['error', 'epochs', 'time']:
        data[stat] = {}
        for ae in acceptable_error:
            data[stat][ae] = {}
            for lr in learning_rate:
                data[stat][ae][lr] = {}
                for m in momentum:
                    data[stat][ae][lr][m] = {}
                    for hs in hidden_size:
                        data[stat][ae][lr][m][hs] = {}
                        for bs in bias_switch:
                            data[stat][ae][lr][m][hs][bs] = {}
                            for ss in set_size:
                                data[stat][ae][lr][m][hs][bs][ss] = 0

    for file in os.listdir(directory):
        filename = os.fsdecode(file)
        filename_split = filename.split('_')
        with open('output/' + filename) as fi:
            lines = fi.readlines()
            data['error'][filename_split[0]][filename_split[1]][filename_split[2]][filename_split[3]][filename_split[4]][filename_split[5]] += float(lines[0])
            data['epochs'][filename_split[0]][filename_split[1]][filename_split[2]][filename_split[3]][filename_split[4]][filename_split[5]] += int(lines[1])
            data['time'][filename_split[0]][filename_split[1]][filename_split[2]][filename_split[3]][filename_split[4]][filename_split[5]] += float(lines[2])

    # ???
    # for stat in data.keys():
    #    for

    return data


if not os.path.exists('charts'):
    os.makedirs('charts')

dt = gather_data()
width = 0.3

for stat in data.keys():
    data = []
    #
    ind = np.arange(1, 8)
    plt.bar(ind - width / 2, data, width, label='data')
    plt.xlabel('x')
    plt.minorticks_on()
    plt.grid(True, which='major', axis='y', ls='--', color='black')
    plt.legend(title='title')
    plt.yscale('linear')
    plt.ylabel('y')
    plt.title('title')
    plt.savefig('charts/a')
    plt.clf()
