from fifteen import Fifteen
from time import time
import sys


if sys.argv[1] == 'bfs':
    f = Fifteen(sys.argv[3])
    start = time()
    board, path, amount = f.bfs(sys.argv[2])
    stop = time()

elif sys.argv[1] == 'dfs':
    f = Fifteen(sys.argv[3])
    start = time()
    board, path, amount = f.dfs(sys.argv[2])
    stop = time()

elif sys.argv[1] == 'astr':
    f = Fifteen(sys.argv[3], sys.argv[2])
    start = time()
    board, path, amount = f.astar()
    stop = time()

print(stop-start)
print(board)
print(path)
print(amount)
