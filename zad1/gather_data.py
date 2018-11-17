import os
import json


def gather_data():
    directory = os.fsencode('./output/')

    # bfs and dfs
    data = {}

    for algorithm in ['bfs', 'dfs']:
        data[algorithm] = {}
        for statistic in ['solution_length', 'visited_states', 'processed_states', 'maximum_depth', 'time']:
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
                    data[filename_split[0]]['solution_length'][filename_split[4]][filename_split[1]] += int(lines[0])
                    data[filename_split[0]]['visited_states'][filename_split[4]][filename_split[1]] += int(lines[1])
                    data[filename_split[0]]['processed_states'][filename_split[4]][filename_split[1]] += int(lines[2])
                    data[filename_split[0]]['maximum_depth'][filename_split[4]][filename_split[1]] += int(lines[3])
                    data[filename_split[0]]['time'][filename_split[4]][filename_split[1]] += float(lines[4])

    for algorithm in data.keys():
        for statistic in data[algorithm].keys():
            for complexity, divisor in zip(data[algorithm][statistic].keys(), [2, 4, 10, 24, 54, 107, 212]):
                for priority in data[algorithm][statistic][complexity].keys():
                    data[algorithm][statistic][complexity][priority] /= divisor
                    data[algorithm][statistic][complexity][priority] = round(data[algorithm][statistic]
                                                                             [complexity][priority], 3)

    # astar
    astr_data = {}

    for statistic in ['solution_length', 'visited_states', 'processed_states', 'maximum_depth', 'time']:
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
                    astr_data['solution_length'][filename_split[4]][filename_split[1]] += int(lines[0])
                    astr_data['visited_states'][filename_split[4]][filename_split[1]] += int(lines[1])
                    astr_data['processed_states'][filename_split[4]][filename_split[1]] += int(lines[2])
                    astr_data['maximum_depth'][filename_split[4]][filename_split[1]] += int(lines[3])
                    astr_data['time'][filename_split[4]][filename_split[1]] += float(lines[4])

    for statistic in astr_data.keys():
        for complexity, divisor in zip(astr_data[statistic].keys(), [2, 4, 10, 24, 54, 107, 212]):
            for heuristic in astr_data[statistic][complexity].keys():
                    astr_data[statistic][complexity][heuristic] /= divisor
                    astr_data[statistic][complexity][heuristic] = round(astr_data[statistic][complexity][heuristic], 3)

    with open('bfs_dfs_data.json', 'w') as fp:
        json.dump(data, fp)
    with open('astr_data.json', 'w') as fp:
        json.dump(astr_data, fp)

    return data, astr_data
