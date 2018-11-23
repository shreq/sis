import subprocess
import os

directory = os.fsencode('./input/')
if not os.path.exists('output'):
    os.makedirs('output')

algorithms = ['astr']   # ['astr', 'bfs', 'dfs']
priorities = ['RDUL', 'RDLU', 'DRUL', 'DRLU', 'LUDR', 'LURD', 'ULDR', 'ULRD']  # ['RDUL', 'RDLU', 'DRUL', 'DRLU', 'LUDR', 'LURD', 'ULDR', 'ULRD']

for algorithm in algorithms:
    print(algorithm)
    if algorithm == 'astr':
        for heuristic in ['manh', 'hamm']:
            print('\t' + heuristic)
            for file in os.listdir(directory):
                filename = os.fsdecode(file)
                #if not os.path.exists('output/' + algorithm + '_' + heuristic + '_solv_' + filename):
                subprocess.call(['python', 'main.py', algorithm, heuristic, 'input/' + filename,
                                 'output/' + algorithm + '_' + heuristic + '_solv_' + filename,
                                 'output/' + algorithm + '_' + heuristic + '_stats_' + filename])
    else:
        for priority in priorities:
            print('\t' + priority)
            for file in os.listdir(directory):
                filename = os.fsdecode(file)
                if not os.path.exists('output/' + algorithm + '_' + priority + '_solv_' + filename):
                    subprocess.call(['python', 'main.py', algorithm, priority, 'input/' + filename,
                                     'output/' + algorithm + '_' + priority + '_solv_' + filename,
                                     'output/' + algorithm + '_' + priority + '_stats_' + filename])
