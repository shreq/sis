import subprocess
import os

directory = os.fsencode('./input/')

for algorithm in ['astr', 'dfs', 'bfs']:
    if algorithm == 'astr':
        for heuristic in ['hamm', 'manh']:
            for file in os.listdir(directory):
                filename = os.fsdecode(file)
                subprocess.call(['python main.py', algorithm, heuristic , filename, 'solv_' + filename, 'stats_' + filename])


