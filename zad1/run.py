import subprocess
import os

directory = os.fsencode('./input/')
if not os.path.exists('output'):
    os.makedirs('output')


for algorithm in ['astr', 'bfs', 'dfs']:
    print(algorithm)
    if algorithm == 'astr':
        for heuristic in ['manh', 'hamm']:
            for file in os.listdir(directory):
                filename = os.fsdecode(file)
                subprocess.call(['python', 'main.py', algorithm, heuristic, 'input/' + filename,
                                 'output/' + algorithm + '_' + heuristic + '_solv_' + filename,
                                 'output/' + algorithm + '_' + heuristic + '_stats_' + filename])
    else:
        for priority in ['RDUL', 'RDLU', 'DRUL', 'DRLU', 'LUDR', 'LURD', 'ULDR', 'ULRD']:
            for file in os.listdir(directory):
                filename = os.fsdecode(file)
                subprocess.call(['python', 'main.py', algorithm, priority, 'input/' + filename,
                                 'output/' + algorithm + '_' + priority + '_solv_' + filename,
                                 'output/' + algorithm + '_' + priority + '_stats_' + filename])
