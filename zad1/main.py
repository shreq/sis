from fifteen import Fifteen
from time import time
import sys

# args:
# 1 [bfs | dfs | astr] algorithm
# 2 [urdl | hamm | manh] priority/heuristic
# 3 starting state file
# 4 solved state file
# 5 stats file

if sys.argv[1] == 'bfs':
    f = Fifteen(sys.argv[3])
    start = time()
    solution_length, visited, processed, max_depth, path, tiles = f.bfs(sys.argv[2])
    stop = time()

elif sys.argv[1] == 'dfs':
    f = Fifteen(sys.argv[3])
    start = time()
    solution_length, visited, processed, max_depth, path, tiles = f.dfs(sys.argv[2])
    stop = time()

elif sys.argv[1] == 'astr':
    f = Fifteen(sys.argv[3], sys.argv[2])
    start = time()
    solution_length, visited, processed, max_depth, path, tiles = f.astar()
    stop = time()

else:
    raise NameError

print(stop - start)
print(tiles)
print(path)
print(solution_length)

with open(sys.argv[4], 'w', encoding='utf-8') as fout:
    fout.write(str(solution_length) + '\n')
    fout.write(path)

with open(sys.argv[5], 'w', encoding='utf-8') as fout:
    fout.write(str(solution_length) + '\n')
    fout.write(str(visited) + '\n')
    fout.write(str(processed) + '\n')
    fout.write(str(max_depth) + '\n')
    fout.write(str(format(stop - start, '.3f')))
