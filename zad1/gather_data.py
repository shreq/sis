import os
import json


def gather_data():
    directory = os.fsencode('./output/')

    # bfs and dfs
    data = {}

    for algorithm in ['bfs', 'dfs']:
        data[algorithm] = {}
        for statistic in ['długość rozwiązania', 'stany odwiedzone', 'stany przetworzone', 'maksymalna głębokość', 'czas [ms]']:
            data[algorithm][statistic] = {}
            for complexity in ['01', '02', '03', '04', '05', '06', '07']:
                data[algorithm][statistic][complexity] = {}
                for priority in ['RDUL', 'RDLU', 'DRUL', 'DRLU', 'LUDR', 'LURD', 'ULDR', 'ULRD']:
                    data[algorithm][statistic][complexity][priority] = 0

    for file in os.listdir(directory):
        filename = os.fsdecode(file)
        filename_split = filename.split('_')
        if filename_split[2] == 'stats':
            if filename_split[0] != 'astr':
                with open('output/' + filename) as fi:
                    lines = fi.readlines()
                    data[filename_split[0]]['długość rozwiązania'][filename_split[4]][filename_split[1]] += int(lines[0])
                    data[filename_split[0]]['stany odwiedzone'][filename_split[4]][filename_split[1]] += int(lines[1])
                    data[filename_split[0]]['stany przetworzone'][filename_split[4]][filename_split[1]] += int(lines[2])
                    data[filename_split[0]]['maksymalna głębokość'][filename_split[4]][filename_split[1]] += int(lines[3])
                    data[filename_split[0]]['czas [ms]'][filename_split[4]][filename_split[1]] += float(lines[4])

    for algorithm in data.keys():
        for statistic in data[algorithm].keys():
            for complexity, divisor in zip(data[algorithm][statistic].keys(), [2, 4, 10, 24, 54, 107, 212]):
                for priority in data[algorithm][statistic][complexity].keys():
                    data[algorithm][statistic][complexity][priority] /= divisor
                    data[algorithm][statistic][complexity][priority] = round(data[algorithm][statistic]
                                                                             [complexity][priority], 3)

    # astar
    astr_data = {}

    for statistic in ['długość rozwiązania', 'stany odwiedzone', 'stany przetworzone', 'maksymalna głębokość', 'czas [ms]']:
        astr_data[statistic] = {}
        for complexity in ['01', '02', '03', '04', '05', '06', '07']:
            astr_data[statistic][complexity] = {}
            for heuristic in ['hamm', 'manh']:
                astr_data[statistic][complexity][heuristic] = 0

    for file in os.listdir(directory):
        filename = os.fsdecode(file)
        filename_split = filename.split('_')
        if filename_split[2] == 'stats':
            if filename_split[0] == 'astr':
                with open('output/' + filename) as fi:
                    lines = fi.readlines()
                    astr_data['długość rozwiązania'][filename_split[4]][filename_split[1]] += int(lines[0])
                    astr_data['stany odwiedzone'][filename_split[4]][filename_split[1]] += int(lines[1])
                    astr_data['stany przetworzone'][filename_split[4]][filename_split[1]] += int(lines[2])
                    astr_data['maksymalna głębokość'][filename_split[4]][filename_split[1]] += int(lines[3])
                    astr_data['czas [ms]'][filename_split[4]][filename_split[1]] += float(lines[4])

    for statistic in astr_data.keys():
        for complexity, divisor in zip(astr_data[statistic].keys(), [2, 4, 10, 24, 54, 107, 212]):
            for heuristic in astr_data[statistic][complexity].keys():
                    astr_data[statistic][complexity][heuristic] /= divisor
                    astr_data[statistic][complexity][heuristic] = round(astr_data[statistic][complexity][heuristic], 3)

    # with open('bfs_dfs_data.json', 'w') as fp:
    #     json.dump(data, fp)
    # with open('astr_data.json', 'w') as fp:
    #     json.dump(astr_data, fp)

    return data, astr_data
