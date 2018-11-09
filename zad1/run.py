import subprocess
import os

directory = os.fsencode('./input/')
if not os.path.exists('output'):
    os.makedirs('output')


for algorithm in ['astr', 'dfs', 'bfs']:
    if algorithm == 'astr':
        for heuristic in ['hamm', 'manh']:
            for file in os.listdir(directory):
                filename = os.fsdecode(file)
                subprocess.call(['python', 'main.py', algorithm, heuristic, 'input/' + filename, 'output/solv_' + filename,
                                 'output/stats_' + filename])
    else:
        for priority in ['RDUL', 'RDLU', 'DRUL', 'DRLU', 'LUDR', 'LURD', 'ULDR', 'ULRD']:
            for file in os.listdir(directory):
                filename = os.fsdecode(file)
                subprocess.call(['python', 'main.py', algorithm, priority, 'input/' + filename, 'output/solv_' + filename,
                                 'output/stats_' + filename])
