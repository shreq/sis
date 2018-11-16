import os
import json


directory = os.fsencode('./output/')

# bfs and dfs
data = {}

for algorithm in ['bfs', 'dfs']:
    data[algorithm] = {}
    for complexity in ['01', '02', '03', '04', '05', '06', '07']:
        data[algorithm][complexity] = {}
        for priority in ['RDUL', 'RDLU', 'DRUL', 'DRLU', 'LUDR', 'LURD', 'ULDR', 'ULRD']:
            data[algorithm][complexity][priority] = {}
            for statistic in ['solution_length', 'visited_states', 'processed_states', 'maximum_depth', 'time']:
                data[algorithm][complexity][priority][statistic] = 0

for file in os.listdir(directory):
    filename = os.fsdecode(file)
    filename_split = filename.split('_')
    if filename_split[2] == 'stats':
        if filename_split[0] != 'astr':
            with open('output/' + filename) as fi:
                lines = fi.readlines()
                data[filename_split[0]][filename_split[4]][filename_split[1]]['solution_length'] += int(lines[0])
                data[filename_split[0]][filename_split[4]][filename_split[1]]['visited_states'] += int(lines[1])
                data[filename_split[0]][filename_split[4]][filename_split[1]]['processed_states'] += int(lines[2])
                data[filename_split[0]][filename_split[4]][filename_split[1]]['maximum_depth'] += int(lines[3])
                data[filename_split[0]][filename_split[4]][filename_split[1]]['time'] += float(lines[4])

for algorithm in data.keys():
    for complexity, divisor in zip(data[algorithm].keys(), [2, 4, 10, 24, 54, 107, 212]):
        for priority in data[algorithm][complexity].keys():
            for statistic in data[algorithm][complexity][priority].keys():
                data[algorithm][complexity][priority][statistic] /= divisor
                data[algorithm][complexity][priority][statistic] = round(data[algorithm][complexity]
                                                                         [priority][statistic], 3)

with open('bfs_dfs_data.json', 'w') as fp:
    json.dump(data, fp)


# astar
astr_data = {}

for complexity in ['01', '02', '03', '04', '05', '06', '07']:
    astr_data[complexity] = {}
    for heuristic in ['hamm', 'manh']:
        astr_data[complexity][heuristic] = {}
        for statistic in ['solution_length', 'visited_states', 'processed_states', 'maximum_depth', 'time']:
            astr_data[complexity][heuristic][statistic] = 0

for file in os.listdir(directory):
    filename = os.fsdecode(file)
    filename_split = filename.split('_')
    if filename_split[2] == 'stats':
        if filename_split[0] == 'astr':
            with open('output/' + filename) as fi:
                lines = fi.readlines()
                astr_data[filename_split[4]][filename_split[1]]['solution_length'] += int(lines[0])
                astr_data[filename_split[4]][filename_split[1]]['visited_states'] += int(lines[1])
                astr_data[filename_split[4]][filename_split[1]]['processed_states'] += int(lines[2])
                astr_data[filename_split[4]][filename_split[1]]['maximum_depth'] += int(lines[3])
                astr_data[filename_split[4]][filename_split[1]]['time'] += float(lines[4])


for complexity, divisor in zip(astr_data.keys(), [2, 4, 10, 24, 54, 107, 212]):
    for priority in astr_data[complexity].keys():
        for statistic in astr_data[complexity][priority].keys():
            astr_data[complexity][priority][statistic] /= divisor
            astr_data[complexity][priority][statistic] = round(astr_data[complexity][priority][statistic], 3)

with open('astr_data.json', 'w') as fp:
    json.dump(astr_data, fp)
